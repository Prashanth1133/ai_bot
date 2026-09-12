from __future__ import annotations

import asyncio
import time

from decimal import Decimal

from app.config import TIMEFRAMES
from app.coin_manager import CoinManager
from app.logger import logger
from exchange.binance_rest import BinanceRestClient
from market.historical import BinanceHistoricalData

from core.websocket import BinanceWebSocket
from core.event_bus import EventBus
from core.orderbook_manager import OrderBookManager

from market.trades import parse_trade
from market.candles import parse_candle
from market.candle_manager import CandleManager
from models.market import Candle
from app.settings import settings


from features.orderflow import OrderFlowEngine
from features.feature_store import FeatureStore
from features.engine import FeatureEngine
from processors.smart_money_processor import SmartMoneyProcessor

from processors.signal_processor import SignalProcessor
from processors.feature_processor import FeatureProcessor
from processors.volume_profile_processor import VolumeProfileProcessor

from processors.multi_timeframe_processor import MultiTimeframeProcessor
from processors.market_regime_processor import MarketRegimeProcessor
from processors.feature_fusion_processor import FeatureFusionProcessor
from processors.sequence_processor import SequenceProcessor

class MarketEngine:
    """
    Professional Market Data Engine

    Responsibilities
    ----------------
    • Receive websocket messages
    • Parse market objects
    • Publish events
    • Maintain local market state
    """

    def __init__(self):

        self.coin = CoinManager()

        self.rest = BinanceRestClient()
        self.historical = BinanceHistoricalData()

        self.bus = EventBus()

        self.market_ws = None
        self.candle_ws = None
        self.candle_ws_task = None

        self.last_closed_candle_time = {}

        self.orderbooks = OrderBookManager()

        self.candles = CandleManager()

        self.orderflow = OrderFlowEngine()

        self.feature_store = FeatureStore()

        self.features = FeatureEngine(
            self.feature_store
        )


        self.smart_money_processor = SmartMoneyProcessor(
            self.candles,
            self.bus
        )

        
        self.feature_processor = FeatureProcessor(
            self.feature_store,
            self.bus
        )

        
        self.signal_processor = SignalProcessor(self.bus)

        from live.signal_engine import LiveSignalEngine

        live_engine = LiveSignalEngine()

        self.signal_processor.set_engine(
            live_engine
        )
        
        self.volume_profile_processor = VolumeProfileProcessor(
            self.bus,
            self.candles
        )

        self.multi_timeframe = MultiTimeframeProcessor(self.bus)

        self.market_regime_processor = MarketRegimeProcessor(
            self.bus
        )

        self.feature_fusion = FeatureFusionProcessor(self.bus)

        self.sequence = SequenceProcessor(self.bus)

        self.bus.subscribe(
            "candle",
            self.smart_money_processor.on_candle
        )

        self.bus.subscribe(
            "candle",
            self.feature_processor.on_closed_candle
        )

        self.bus.subscribe(
            "candle",
            self.volume_profile_processor.on_candle
        )

        self.bus.subscribe(
            "feature_sequence",
            self.signal_processor.on_features
        )

        self.bus.subscribe(
            "market_state",
            self.multi_timeframe.on_market_state
        )

        self.bus.subscribe(
            "features",
            self.market_regime_processor.on_features
        )
        
        self.bus.subscribe(
            "fusion_request",
            self.feature_fusion.on_update
        )

        from processors.unified_pipeline_processor import UnifiedPipelineProcessor

        self.unified_pipeline = UnifiedPipelineProcessor(
            self.bus,
            self.candles,
            self.orderflow,
            self.features,
        )

        self.bus.subscribe(
            "candle",
            self.unified_pipeline.on_candle
        )

        self.bus.subscribe(
            "fused_feature_sequence",
            self.signal_processor.on_features
        )

        self.bus.subscribe(
            "feature_vector",
            self.sequence.on_feature_vector
        )

    @property
    def active_symbol(self) -> str:
        return settings.ACTIVE_SYMBOL

    @property
    def ai_timeframe(self) -> str:
        return settings.MODEL_TIMEFRAME

    async def handler(self, message: dict):
        """
        Dispatch websocket messages.
        """

        stream = message.get("stream", "")

        try:

            if "@trade" in stream:

                await self.handle_trade(message)

            elif "@depth" in stream:

                await self.handle_depth(message)

            elif "@kline" in stream:

                await self.handle_kline(message)

        except Exception:

            logger.exception(
                "Error processing websocket message."
            )

    async def handle_trade(self, message: dict):
        """
        Handle trade stream.
        """

        trade = parse_trade(message)

        if trade.price <= 0 or trade.quantity <= 0:

            logger.warning(
                f"[TRADE FILTER] Ignoring invalid trade "
                f"{trade.symbol} "
                f"price={trade.price} "
                f"quantity={trade.quantity}"
            )

            return

        latency = (
            time.time() * 1000
            - trade.timestamp
        )

        metrics = self.orderflow.process_trade(
            trade
        )

        self.features.update_orderflow(
            trade.symbol,
            metrics
        )

        self.features.update(
            trade.symbol,
            "last_price",
            float(trade.price)
        )

        self.features.update(
            trade.symbol,
            "orderflow",
            metrics
        )

        await self.bus.publish(
            "trade",
            trade
        )

        await self.bus.publish(
            "orderflow",
            metrics
        )

        await self.bus.publish(
            "latency",
            latency
        )

    async def handle_depth(self, message: dict):
        """
        Handle orderbook updates.
        """

        orderbook = await self.orderbooks.update(
            message
        )

        if orderbook is None:
            return

        self.features.update_orderbook(
            orderbook.symbol,
            orderbook
        )

        self.features.update(
            orderbook.symbol,
            "orderbook",
            orderbook
        )

        await self.bus.publish(
            "orderbook",
            orderbook
        )

    async def handle_kline(self, message: dict):
        """
        Handle candle updates.

        The AI model timeframe is received through the
        dedicated candle websocket.
        """

        candle = parse_candle(message)

        if candle.closed:

            last_processed = self.last_closed_candle_time.get(
                candle.symbol
            )

            if last_processed == candle.close_time:

                logger.debug(
                    f"[CANDLE DUPLICATE] {candle.symbol} "
                    f"{candle.interval} close_time={candle.close_time}"
                )

                return

        self.candles.update(candle)

        # -------------------------------------------------
        # Log every closed AI candle
        # -------------------------------------------------

        if candle.closed:

            if candle.interval == self.ai_timeframe:

                logger.success(
                    f"[AI CANDLE CLOSED] "
                    f"{candle.symbol} "
                    f"{candle.interval} "
                    f"close={candle.close} "
                    f"close_time={candle.close_time}"
                )

            if hasattr(self.features, "update_candle"):

                self.features.update_candle(
                    candle
                )

        # -------------------------------------------------
        # Publish candle
        # -------------------------------------------------

        await self.bus.publish(
            "candle",
            candle
        )

        if candle.closed:

            self.last_closed_candle_time[candle.symbol] = (
                candle.close_time
            )

    async def reconcile_latest_candle(self):
        """
        Verify that the latest closed model-timeframe candle
        is present after websocket connection/reconnection.

        This protects the AI pipeline from missing a candle-close
        websocket event during a disconnect/reconnect.
        """

        symbol = self.active_symbol
        timeframe = self.ai_timeframe

        try:

            candles = await asyncio.to_thread(
                self.historical.fetch_klines,
                symbol,
                timeframe,
                2,
            )

            if not candles:
                logger.warning(
                    f"[CANDLE RECONCILE] "
                    f"No candles returned for "
                    f"{symbol} {timeframe}"
                )
                return

            # Binance returns the newest candle last.
            latest = candles[-1]

            # -------------------------------------------------
            # Only process a CLOSED candle
            # -------------------------------------------------

            if not latest.closed:

                if len(candles) < 2:
                    return

                latest = candles[-2]

            # -------------------------------------------------
            # Check duplicate by close_time
            # -------------------------------------------------

            last_processed = self.last_closed_candle_time.get(
                symbol
            )

            if last_processed == latest.close_time:

                logger.debug(
                    f"[CANDLE DUPLICATE] {symbol} "
                    f"{timeframe} close_time={latest.close_time}"
                )

                return

            # -------------------------------------------------
            # Check existing candle
            # -------------------------------------------------

            existing = self.candles.latest(
                symbol,
                timeframe,
            )

            if (
                existing is not None
                and existing.close_time >= latest.close_time
            ):
                return

            logger.warning(
                f"[CANDLE RECOVERY] "
                f"Recovering {symbol} {timeframe} "
                f"close={latest.close} "
                f"close_time={latest.close_time}"
            )

            # -------------------------------------------------
            # Insert into candle manager
            # -------------------------------------------------

            self.candles.update(latest)

            # -------------------------------------------------
            # Update feature engine
            # -------------------------------------------------

            if hasattr(self.features, "update_candle"):

                self.features.update_candle(
                    latest
                )

            # -------------------------------------------------
            # Send through the SAME event pipeline as WS
            # -------------------------------------------------

            await self.bus.publish(
                "candle",
                latest,
            )

            self.last_closed_candle_time[symbol] = (
                latest.close_time
            )

            logger.success(
                f"[CANDLE RECOVERY COMPLETE] "
                f"{symbol} {timeframe} "
                f"close_time={latest.close_time}"
            )

        except Exception:

            logger.exception(
                "[CANDLE RECONCILE] Failed"
            )

    async def warmup_model(self):
        """
        Bootstrap the model sequence with historical candles.

        This prevents the application from waiting for
        128 live 5-minute candles.
        """

        symbol = self.active_symbol
        timeframe = self.ai_timeframe

        logger.info(
            f"[WARMUP] Loading historical data for "
            f"{symbol} {timeframe}"
        )

        candles = await asyncio.to_thread(
            self.historical.fetch_klines,
            symbol,
            timeframe,
            settings.HISTORICAL_WARMUP_CANDLES,
        )

        vectors = []

        for candle in candles:

            vector = self.feature_processor.build_historical_vector(
                candle
            )

            if vector is not None:
                vectors.append(vector)

        required = settings.MODEL_SEQUENCE_LENGTH

        if len(vectors) < required:

            raise RuntimeError(
                f"[WARMUP] Required {required} "
                f"vectors but only {len(vectors)} available"
            )

        vectors = vectors[-required:]

        self.sequence.warmup(
            symbol,
            timeframe,
            vectors,
        )

        for tf in ["1m", "5m", "15m", "1h", "4h"]:
            try:
                tf_candles = await asyncio.to_thread(
                    self.historical.fetch_klines,
                    symbol,
                    tf,
                    100,
                )
                self.unified_pipeline.mtf_manager.update_history(symbol, tf, tf_candles)
            except Exception as e:
                logger.warning(f"[MTF WARMUP] Failed for {symbol} {tf}: {e}")

        logger.success(
            f"[WARMUP COMPLETE] "
            f"{symbol} {timeframe} "
            f"{len(vectors)}/{required} vectors ready"
        )

    async def start(self):
        """
        Start Market Engine.

        Dedicated connections:
        -----------------------
        1. Market websocket:
           - trade
           - orderbook

        2. Candle websocket:
           - model timeframe only (5m)

        The candle connection is isolated so high-frequency
        market traffic cannot interfere with the AI candle pipeline.
        """

        await self.warmup_model()

        # ============================================================
        # AI CANDLE WEBSOCKET
        # ============================================================

        candle_stream = (
            f"{self.active_symbol.lower()}"
            f"@kline_{self.ai_timeframe}"
        )

        self.candle_ws = BinanceWebSocket(
            streams=[candle_stream],
            handler=self.handler,
            name="AI-CANDLE",
            reconnect_handler=self.reconcile_latest_candle,
        )

        logger.success(
            f"[CANDLE WS] {self.active_symbol} "
            f"{self.ai_timeframe} dedicated candle connection created"
        )

        # Start the candle connection FIRST.
        self.candle_ws_task = asyncio.create_task(
            self.candle_ws.start(),
            name="ai-candle-websocket",
        )

        # ------------------------------------------------------------
        # WAIT UNTIL THE SOCKET IS ACTUALLY CONNECTED
        # ------------------------------------------------------------

        for _ in range(100):

            if self.candle_ws.connected:
                break

            await asyncio.sleep(0.05)

        else:

            raise RuntimeError(
                f"[CANDLE WS] Failed to connect "
                f"{self.active_symbol} "
                f"{self.ai_timeframe}"
            )

        logger.success(
            f"[CANDLE WS] Connected before candle reconciliation: "
            f"{self.active_symbol} {self.ai_timeframe}"
        )

        # ============================================================
        # NOW RECOVER THE LATEST CLOSED CANDLE
        # ============================================================

        await self.reconcile_latest_candle()

        # ============================================================
        # CONNECTION 1: HIGH-FREQUENCY MARKET DATA
        # ============================================================

        market_streams = [
            f"{self.active_symbol.lower()}@trade",
            f"{self.active_symbol.lower()}@depth20@100ms",
        ]

        self.market_ws = BinanceWebSocket(
            streams=market_streams,
            handler=self.handler,
            name="MARKET",
        )

        logger.success(
            f"[MARKET WS] "
            f"{self.active_symbol.upper()} "
            f"trade + orderbook connection created"
        )

        logger.success(
            f"[MARKET ENGINE] "
            f"Active symbol={self.active_symbol.upper()} "
            f"AI timeframe={self.ai_timeframe}"
        )

        # ============================================================
        # RUN BOTH CONNECTIONS
        # ============================================================

        await asyncio.gather(
            self.candle_ws_task,
            self.market_ws.start(),
        )

