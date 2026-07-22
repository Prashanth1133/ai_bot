from __future__ import annotations

import asyncio
import time
from typing import Awaitable, Callable

import orjson
import websockets
from loguru import logger
from tenacity import retry, stop_never, wait_exponential
from websockets.exceptions import ConnectionClosed

BINANCE_WS = "wss://fstream.binance.com/stream"


class BinanceWebSocket:
    """
    Professional Binance WebSocket Client

    Features
    --------
    - Automatic reconnect
    - Heartbeat monitoring
    - Exponential backoff
    - Async-safe reconnect
    - Graceful shutdown
    """

    def __init__(
        self,
        streams: list[str],
        handler: Callable[[dict], Awaitable[None]],
    ):

        self.streams = streams
        self.handler = handler

        self.ws = None

        self.connected = False

        self.running = True

        self.last_message = time.time()

        self.reconnect_lock = asyncio.Lock()

    @property
    def url(self) -> str:

        stream = "/".join(self.streams)

        return f"{BINANCE_WS}?streams={stream}"

    @retry(
        wait=wait_exponential(multiplier=1, min=1, max=30),
        stop=stop_never,
        reraise=True,
    )
    async def connect(self):

        logger.info(f"Connecting -> {self.url}")

        self.ws = await websockets.connect(
            self.url,
            ping_interval=20,
            ping_timeout=20,
            max_size=10_000_000,
            compression=None,
        )

        self.connected = True

        self.last_message = time.time()

        logger.success("Connected to Binance")

    async def receive(self):

        while self.running:

            try:

                raw = await self.ws.recv()

                self.last_message = time.time()

                message = orjson.loads(raw)

                await self.handler(message)

            except ConnectionClosed:

                logger.warning("Connection closed.")

                await self.reconnect()

            except Exception as e:

                logger.exception(e)

                await self.reconnect()

    async def heartbeat(self):

        while self.running:

            await asyncio.sleep(15)

            if not self.connected:
                continue

            elapsed = time.time() - self.last_message

            if elapsed > 30:

                logger.warning(
                    f"No data received for {elapsed:.1f}s"
                )

                await self.reconnect()

    async def reconnect(self):

        async with self.reconnect_lock:

            if self.connected is False:
                return

            self.connected = False

            logger.warning("Reconnecting...")

            try:

                if self.ws:

                    await self.ws.close()

            except Exception as e:

                logger.exception(e)

            await self.connect()

    async def shutdown(self):

        logger.info("Stopping websocket...")

        self.running = False

        self.connected = False

        if self.ws:

            await self.ws.close()

    async def start(self):

        await self.connect()

        receiver = asyncio.create_task(self.receive())

        heartbeat = asyncio.create_task(self.heartbeat())

        await asyncio.gather(
            receiver,
            heartbeat,
        )