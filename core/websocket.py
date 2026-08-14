from __future__ import annotations

import asyncio
import time
from typing import Awaitable, Callable, Optional

import orjson
import websockets
from loguru import logger
from websockets.exceptions import ConnectionClosed


BINANCE_WS = "wss://fstream.binance.com/stream"
HEARTBEAT_INTERVAL = 15.0
MESSAGE_TIMEOUT = 360.0  # 6 minutes


class BinanceWebSocket:
    """
    Professional Binance Futures WebSocket Client.

    Responsibilities
    ----------------
    - Connect to the currently selected streams only
    - Automatically reconnect after connection failure
    - Prevent multiple simultaneous reconnect attempts
    - Heartbeat / stale connection detection
    - Graceful shutdown
    - Safe task cancellation
    - Preserve the active symbol streams during reconnect

    IMPORTANT
    ---------
    This class does NOT discover or subscribe to Binance symbols.

    The MarketEngine supplies the exact streams.

    Example:

        btcusdt@trade
        btcusdt@depth20@100ms
        btcusdt@kline_1m
        btcusdt@kline_5m
        btcusdt@kline_15m
        btcusdt@kline_1h
        btcusdt@kline_4h

    Therefore, if BTCUSDT is active, only BTCUSDT is received.
    """

    def __init__(
        self,
        streams: list[str],
        handler: Callable[[dict], Awaitable[None]],
        name: str = "websocket",
        reconnect_handler: Callable[[], Awaitable[None]] | None = None,
    ):

        # ---------------------------------------------------------
        # Stream configuration
        # ---------------------------------------------------------

        self.streams = list(streams)

        self.handler = handler

        self.name = name

        self.reconnect_handler = reconnect_handler

        # ---------------------------------------------------------
        # WebSocket state
        # ---------------------------------------------------------

        self.ws = None

        self.connected = False

        self.running = False

        self.last_message = time.monotonic()

        # ---------------------------------------------------------
        # Synchronization
        # ---------------------------------------------------------

        self.reconnect_lock = asyncio.Lock()

        # Used to wake/stop connection loops.
        self._stop_event = asyncio.Event()

        # Signals that current connection should be terminated.
        self._disconnect_event = asyncio.Event()

        # ---------------------------------------------------------
        # Reconnect configuration
        # ---------------------------------------------------------

        self.reconnect_delay = 1.0

        self.max_reconnect_delay = 30.0

        # ---------------------------------------------------------
        # Heartbeat configuration
        # ---------------------------------------------------------

        self.heartbeat_interval = HEARTBEAT_INTERVAL

        self.connection_timeout = MESSAGE_TIMEOUT

    # =============================================================
    # URL
    # =============================================================

    @property
    def url(self) -> str:

        if not self.streams:
            raise ValueError(
                "BinanceWebSocket requires at least one stream."
            )

        stream = "/".join(
            stream.lower()
            for stream in self.streams
        )

        return f"{BINANCE_WS}?streams={stream}"

    # =============================================================
    # CONNECT
    # =============================================================

    async def connect(self) -> bool:

        if not self.running:
            return False

        logger.info(
            f"[{self.name}] Connecting -> {self.url}"
        )

        try:

            ws = await websockets.connect(

                self.url,

                ping_interval=20,

                ping_timeout=20,

                close_timeout=5,

                max_size=10_000_000,

                compression=None,
            )

            # -----------------------------------------------------
            # Replace old socket safely.
            # -----------------------------------------------------

            old_ws = self.ws

            self.ws = ws

            self.connected = True

            self.last_message = time.monotonic()

            self._disconnect_event.clear()

            # -----------------------------------------------------
            # Successful connection resets backoff.
            # -----------------------------------------------------

            self.reconnect_delay = 1.0

            if old_ws is not None:

                try:

                    await old_ws.close()

                except Exception:

                    pass

            logger.success(
                f"[{self.name}] Connected to Binance"
            )

            return True

        except asyncio.CancelledError:

            raise

        except Exception as exc:

            self.connected = False

            logger.error(
                f"[{self.name}] Binance connection failed: {exc}"
            )

            return False

    # =============================================================
    # RECEIVE
    # =============================================================

    async def receive(self) -> bool:
        """
        Receive messages from the current socket.

        IMPORTANT:
        This method does NOT call reconnect().

        The outer start() loop owns reconnection.
        This prevents recursive/multiple reconnect attempts.
        """

        if self.ws is None:

            return False

        current_ws = self.ws

        while self.running:

            try:

                raw = await current_ws.recv()

                if raw is None:

                    logger.warning(
                        "Binance returned an empty message."
                    )

                    return False

                self.last_message = time.monotonic()

                # -------------------------------------------------
                # Binance normally sends text frames.
                # Handle bytes too.
                # -------------------------------------------------

                if isinstance(raw, bytes):

                    message = orjson.loads(raw)

                else:

                    message = orjson.loads(
                        raw.encode()
                    )

                # -------------------------------------------------
                # Pass message to MarketEngine.
                # -------------------------------------------------

                await self.handler(message)

            except asyncio.CancelledError:

                raise

            except ConnectionClosed as exc:

                logger.warning(
                    f"[{self.name}] Connection closed: "
                    f"code={exc.code} "
                    f"reason={exc.reason}"
                )

                return False

            except Exception as exc:

                logger.exception(
                    f"WebSocket receive error: {exc}"
                )

                return False

        return False

    # =============================================================
    # HEARTBEAT
    # =============================================================

    async def heartbeat(self):

        while self.running:

            try:

                await asyncio.sleep(
                    self.heartbeat_interval
                )

                if not self.connected:
                    continue

                elapsed = (
                    time.monotonic()
                    - self.last_message
                )

                if elapsed > self.connection_timeout:

                    logger.warning(
                        f"[{self.name}] WebSocket appears stale. "
                        f"No data for {elapsed:.1f}s (limit={self.connection_timeout:.1f}s), reconnecting..."
                    )

                    self._disconnect_event.set()

                    # -------------------------------------------------
                    # Closing the socket causes receive() to return.
                    # The start() loop will reconnect exactly once.
                    # -------------------------------------------------

                    if self.ws is not None:

                        try:

                            await self.ws.close()

                        except Exception as exc:

                            logger.debug(
                                f"Heartbeat close error: {exc}"
                            )

                    return

            except asyncio.CancelledError:

                return

            except Exception as exc:

                logger.exception(
                    f"Heartbeat error: {exc}"
                )

    # =============================================================
    # CLOSE CURRENT CONNECTION
    # =============================================================

    async def _close_current_connection(self):

        ws = self.ws

        self.ws = None

        self.connected = False

        if ws is not None:

            try:

                await ws.close()

            except Exception as exc:

                logger.debug(
                    f"Socket close error: {exc}"
                )

    # =============================================================
    # RECONNECT
    # =============================================================

    async def reconnect(self) -> bool:
        """
        Perform exactly one reconnect attempt.

        This method is protected by reconnect_lock.

        It is intentionally NOT called recursively from receive().
        """

        async with self.reconnect_lock:

            if not self.running:

                return False

            # -----------------------------------------------------
            # If another task already restored the connection,
            # don't reconnect again.
            # -----------------------------------------------------

            if self.connected:

                return True

            logger.warning(
                f"[{self.name}] Reconnecting to Binance..."
            )

            await self._close_current_connection()

            delay = self.reconnect_delay

            logger.info(
                f"[{self.name}] Reconnect delay: {delay:.1f}s"
            )

            try:

                await asyncio.wait_for(

                    self._stop_event.wait(),

                    timeout=delay,

                )

                # Stop event was triggered.

                return False

            except asyncio.TimeoutError:

                pass

            if not self.running:

                return False

            success = await self.connect()

            if success:

                logger.success(
                    f"[{self.name}] Binance WebSocket reconnected."
                )

                self.reconnect_delay = 1.0

                if self.reconnect_handler:

                    try:

                        await self.reconnect_handler()

                    except Exception:

                        logger.exception(
                            f"[{self.name}] "
                            f"Reconnect recovery failed"
                        )

                return True

            # -----------------------------------------------------
            # Increase backoff only after failure.
            # -----------------------------------------------------

            self.reconnect_delay = min(

                self.reconnect_delay * 2,

                self.max_reconnect_delay,

            )

            return False

    # =============================================================
    # UPDATE STREAMS
    # =============================================================

    async def update_streams(
        self,
        streams: list[str],
    ):
        """
        Change the active streams.

        Used when the user switches:

            BTCUSDT -> ETHUSDT

        The old BTC connection is closed before ETH is connected.

        This guarantees that both symbols are not simultaneously
        streamed by this WebSocket instance.
        """

        async with self.reconnect_lock:

            if not streams:

                raise ValueError(
                    "At least one Binance stream is required."
                )

            new_streams = list(streams)

            logger.info(
                f"Updating Binance streams: "
                f"{new_streams}"
            )

            self.streams = new_streams

            self._disconnect_event.set()

            await self._close_current_connection()

            self._disconnect_event.clear()

            if self.running:

                await self.connect()

    # =============================================================
    # SHUTDOWN
    # =============================================================

    async def shutdown(self):

        logger.info(
            f"[{self.name}] Stopping Binance WebSocket..."
        )

        self.running = False

        self.connected = False

        self._stop_event.set()

        self._disconnect_event.set()

        await self._close_current_connection()

        logger.info(
            f"[{self.name}] Binance WebSocket stopped."
        )

    # =============================================================
    # START
    # =============================================================

    async def start(self):

        if self.running:

            logger.warning(
                f"[{self.name}] Binance WebSocket is already running."
            )

            return

        self.running = True

        self._stop_event.clear()

        self._disconnect_event.clear()

        # ---------------------------------------------------------
        # Initial connection.
        # ---------------------------------------------------------

        while self.running:

            connected = await self.connect()

            if connected:

                break

            delay = self.reconnect_delay

            logger.warning(
                f"Initial connection failed. "
                f"Retrying in {delay:.1f}s."
            )

            try:

                await asyncio.wait_for(

                    self._stop_event.wait(),

                    timeout=delay,

                )

                return

            except asyncio.TimeoutError:

                pass

            self.reconnect_delay = min(

                self.reconnect_delay * 2,

                self.max_reconnect_delay,

            )

        # ---------------------------------------------------------
        # Main connection supervisor.
        # ---------------------------------------------------------

        while self.running:

            receiver = None

            heartbeat = None

            try:

                if not self.connected:

                    success = await self.reconnect()

                    if not success:

                        continue

                # -------------------------------------------------
                # Start receiver.
                # -------------------------------------------------

                receiver = asyncio.create_task(
                    self.receive(),
                    name="binance-websocket-receiver",
                )

                # -------------------------------------------------
                # Start heartbeat.
                # -------------------------------------------------

                heartbeat = asyncio.create_task(
                    self.heartbeat(),
                    name="binance-websocket-heartbeat",
                )

                # -------------------------------------------------
                # Wait until receiver exits.
                #
                # Reconnect is handled ONLY here.
                # -------------------------------------------------

                await receiver

            except asyncio.CancelledError:

                raise

            except Exception as exc:

                logger.exception(
                    f"WebSocket supervisor error: {exc}"
                )

            finally:

                # -------------------------------------------------
                # Stop heartbeat.
                # -------------------------------------------------

                if heartbeat is not None:

                    heartbeat.cancel()

                    try:

                        await heartbeat

                    except asyncio.CancelledError:

                        pass

                    except Exception:

                        pass

                # -------------------------------------------------
                # Stop receiver if still alive.
                # -------------------------------------------------

                if receiver is not None:

                    if not receiver.done():

                        receiver.cancel()

                        try:

                            await receiver

                        except asyncio.CancelledError:

                            pass

                        except Exception:

                            pass

                # -------------------------------------------------
                # Close current socket.
                # -------------------------------------------------

                await self._close_current_connection()

            # -----------------------------------------------------
            # If shutdown was requested, leave immediately.
            # -----------------------------------------------------

            if not self.running:

                break

            # -----------------------------------------------------
            # Reconnect.
            # -----------------------------------------------------

            await self.reconnect()

        logger.info(
            "Binance WebSocket supervisor stopped."
        )