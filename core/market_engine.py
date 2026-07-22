from __future__ import annotations

import time

from app.config import SYMBOLS, TIMEFRAMES
from app.logger import logger

from core.websocket import BinanceWebSocket
from core.event_bus import EventBus
from core.orderbook_manager import OrderBookManager

from market.trades import parse_trade
from market.candles import parse_candle
from market.candle_manager import CandleManager

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

        self.bus = EventBus()

        self.ws = None

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

        from ai.models.model_manager import ModelManager
        from live.signal_engine import LiveSignalEngine

        manager = ModelManager()

        model = manager.load_latest()

        live_engine = LiveSignalEngine(model)

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
            "feature_vector",
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

        self.bus.subscribe(
            "feature_vector",
            self.sequence.on_feature_vector
        )

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

        await self.bus.publish(
            "orderbook",
            orderbook
        )

    async def handle_kline(self, message: dict):
        """
        Handle candle updates.
        """

        candle = parse_candle(message)

        self.candles.update(candle)

        if candle.closed:

            if hasattr(self.features, "update_candle"):

                self.features.update_candle(
                    candle
                )

        await self.bus.publish(
            "candle",
            candle
        )

        

    async def start(self):
        """
        Start Market Engine.
        """

        streams = []

        for symbol in SYMBOLS:

            logger.info(
                f"Preparing streams for {symbol.upper()}"
            )

            streams.append(
                f"{symbol}@trade"
            )

            streams.append(
                f"{symbol}@depth20@100ms"
            )

            for tf in TIMEFRAMES:

                streams.append(
                    f"{symbol}@kline_{tf}"
                )

        logger.info(
            f"Opening websocket with {len(streams)} streams..."
        )

        self.ws = BinanceWebSocket(

            streams=streams,

            handler=self.handler

        )

        logger.success(
            "Market Engine Started"
        )

        await self.ws.start()