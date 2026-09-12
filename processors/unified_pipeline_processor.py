from __future__ import annotations

from collections import defaultdict, deque
import numpy as np

from app.settings import settings
from logs.log_manager import pipeline_logger
from context.context_builder import ContextBuilder
from context.context_registry import ContextRegistry
from context.context_providers import (
    MTFContextProvider,
    SRContextProvider,
    PatternContextProvider,
    SMCContextProvider,
    OrderFlowContextProvider,
    NewsContextProvider,
    VolumeProfileContextProvider,
    MarketRegimeContextProvider,
    DerivativesContextProvider,
    OnChainContextProvider,
)
from multi_timeframe.multi_timeframe_manager import MultiTimeframeManager
from indicators.support_resistance import SupportResistanceEngine
from patterns.engine import PatternEngine
from smart_money.engine import SmartMoneyEngine
from volume_profile.engine import VolumeProfileEngine
from market_regime.engine import MarketRegimeEngine
from derivatives.engine import DerivativesEngine
from onchain.processor import OnChainProcessor
from feature_fusion.fusion_engine import FeatureFusionEngine
from feature_fusion.schema import UNIFIED_FEATURE_SCHEMA
from decision.rich_output_formatter import RichSignalFormatter


class UnifiedPipelineProcessor:
    """
    Coordinates the complete multi-factor market intelligence pipeline:
    Multi-Timeframe + Support/Resistance + Patterns + SMC + Order Flow + Volume Profile + 
    Market Regime + Derivatives + On-Chain + News -> MarketContext -> FeatureFusionEngine -> 
    Unified Fused Vector (dim=48) & 3D Rolling Sequence Tensor shape=(1, 128, 48).
    """

    def __init__(self, bus, candle_manager, orderflow_engine, feature_engine):
        self.bus = bus
        self.candle_manager = candle_manager
        self.orderflow_engine = orderflow_engine
        self.feature_engine = feature_engine

        # Initialize analytical engines
        self.mtf_manager = MultiTimeframeManager()
        self.sr_engine = SupportResistanceEngine()
        self.pattern_engine = PatternEngine()
        self.smc_engine = SmartMoneyEngine()
        self.vp_engine = VolumeProfileEngine()
        self.regime_engine = MarketRegimeEngine()
        self.derivs_engine = DerivativesEngine()
        self.onchain_processor = OnChainProcessor()
        self.fusion_engine = FeatureFusionEngine()

        # Rolling 48-feature sequence buffer per symbol
        self.fused_sequences = defaultdict(
            lambda: deque(maxlen=settings.MODEL_SEQUENCE_LENGTH)
        )

        # Build Context Registry & Register ALL 10 Providers
        self.registry = ContextRegistry()
        self.registry.register("mtf", MTFContextProvider(self.mtf_manager))
        self.registry.register("sr", SRContextProvider(self.sr_engine, self.candle_manager))
        self.registry.register("patterns", PatternContextProvider(self.pattern_engine, self.candle_manager))
        self.registry.register("smc", SMCContextProvider(self.smc_engine, self.candle_manager))
        self.registry.register("orderflow", OrderFlowContextProvider(self.orderflow_engine, self.feature_engine))
        self.registry.register("volume_profile", VolumeProfileContextProvider(self.vp_engine, self.candle_manager))
        self.registry.register("regime", MarketRegimeContextProvider(self.regime_engine))
        self.registry.register("derivatives", DerivativesContextProvider(self.derivs_engine))
        self.registry.register("onchain", OnChainContextProvider(self.onchain_processor))
        self.registry.register("news", NewsContextProvider())

        self.context_builder = ContextBuilder(self.registry)

    def log_vector_validation(self, symbol: str, vector: np.ndarray) -> None:
        """
        Logs feature semantic breakdown and vector statistics (min, max, mean, std, NaNs, Infs).
        """
        nan_count = int(np.isnan(vector).sum())
        inf_count = int(np.isinf(vector).sum())
        min_val = float(np.min(vector))
        max_val = float(np.max(vector))
        mean_val = float(np.mean(vector))
        std_val = float(np.std(vector))

        pipeline_logger.info(
            f"[FEATURE VALIDATION] {symbol} dim={len(vector)} | "
            f"NaNs={nan_count} Infs={inf_count} | "
            f"min={min_val:.4f} max={max_val:.4f} mean={mean_val:.4f} std={std_val:.4f}"
        )

    async def on_candle(self, candle) -> None:
        """
        Ingest closed candle, update multi-timeframe engine, build unified snapshot and rolling sequence.
        """
        if not candle.closed:
            return

        # Update MTF manager
        self.mtf_manager.update_candle(candle)

        if candle.interval != settings.MODEL_TIMEFRAME:
            return

        # Build complete MarketContext snapshot
        snapshot = self.context_builder.build(candle.symbol, candle.interval)

        # Build fused feature vector adhering to UNIFIED_FEATURE_SCHEMA
        vector = self.fusion_engine.build_from_snapshot(snapshot)

        # Log vector statistics & validation
        self.log_vector_validation(candle.symbol, vector)

        # Maintain rolling 48-feature AI sequence
        key = (candle.symbol, candle.interval)
        self.fused_sequences[key].append(vector)

        # Log rich auditable analysis block
        RichSignalFormatter.log_signal(snapshot)

        # Publish unified market context & fused vector events
        await self.bus.publish(
            "unified_market_context",
            {
                "snapshot": snapshot,
                "vector": vector,
            },
        )

        await self.bus.publish(
            "fused_feature_vector",
            {
                "symbol": candle.symbol,
                "interval": candle.interval,
                "vector": vector,
            },
        )

        # Check if rolling 48-feature sequence is ready for AI Inference
        if len(self.fused_sequences[key]) >= settings.MODEL_SEQUENCE_LENGTH:
            seq_array = np.asarray(self.fused_sequences[key], dtype=np.float32)
            tensor_3d = np.expand_dims(seq_array, axis=0)  # shape: (1, 128, 48)

            pipeline_logger.info(
                f"[FUSED SEQUENCE READY] {candle.symbol} {candle.interval} "
                f"shape={tensor_3d.shape}"
            )

            await self.bus.publish(
                "fused_feature_sequence",
                {
                    "symbol": candle.symbol,
                    "interval": candle.interval,
                    "values": tensor_3d,
                },
            )
