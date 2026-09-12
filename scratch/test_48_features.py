import numpy as np
from market.historical import BinanceHistoricalData
from market.candle_manager import CandleManager
from multi_timeframe.multi_timeframe_manager import MultiTimeframeManager
from features.orderflow import OrderFlowEngine
from features.engine import FeatureEngine
from features.feature_store import FeatureStore
from indicators.support_resistance import SupportResistanceEngine
from patterns.engine import PatternEngine
from smart_money.engine import SmartMoneyEngine
from volume_profile.engine import VolumeProfileEngine
from market_regime.engine import MarketRegimeEngine
from derivatives.engine import DerivativesEngine
from onchain.processor import OnChainProcessor
from feature_fusion.fusion_engine import FeatureFusionEngine
from feature_fusion.schema import UNIFIED_FEATURE_SCHEMA, NUM_UNIFIED_FEATURES
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

def test_feature_variance():
    historical = BinanceHistoricalData()
    candles_1m = historical.fetch_klines("BTCUSDT", "1m", 1000)
    candles_5m = historical.fetch_klines("BTCUSDT", "5m", 300)
    candles_15m = historical.fetch_klines("BTCUSDT", "15m", 100)
    candles_1h = historical.fetch_klines("BTCUSDT", "1h", 50)
    candles_4h = historical.fetch_klines("BTCUSDT", "4h", 20)
    
    tf_candles_dict = {
        "5m": candles_5m,
        "15m": candles_15m,
        "1h": candles_1h,
        "4h": candles_4h,
    }
    mtf_pointers = {tf: 0 for tf in ["5m", "15m", "1h", "4h"]}

    candle_manager = CandleManager()
    mtf_manager = MultiTimeframeManager()
    orderflow = OrderFlowEngine()
    store = FeatureStore()
    features = FeatureEngine(store)
    sr_engine = SupportResistanceEngine()
    pattern_engine = PatternEngine()
    smc_engine = SmartMoneyEngine()
    vp_engine = VolumeProfileEngine()
    regime_engine = MarketRegimeEngine()
    derivs_engine = DerivativesEngine()
    onchain_processor = OnChainProcessor()
    fusion_engine = FeatureFusionEngine()

    registry = ContextRegistry()
    registry.register("mtf", MTFContextProvider(mtf_manager))
    registry.register("sr", SRContextProvider(sr_engine, candle_manager))
    registry.register("patterns", PatternContextProvider(pattern_engine, candle_manager))
    registry.register("smc", SMCContextProvider(smc_engine, candle_manager))
    registry.register("orderflow", OrderFlowContextProvider(orderflow, features))
    registry.register("volume_profile", VolumeProfileContextProvider(vp_engine, candle_manager))
    registry.register("regime", MarketRegimeContextProvider(regime_engine))
    registry.register("derivatives", DerivativesContextProvider(derivs_engine))
    registry.register("onchain", OnChainContextProvider(onchain_processor))
    registry.register("news", NewsContextProvider())

    builder = ContextBuilder(registry)

    matrix = []
    for c in candles_1m:
        candle_manager.update(c)
        mtf_manager.update_candle(c)
        orderflow.process_candle(c)

        curr_close_time = getattr(c, "close_time", 0)
        for tf in ["5m", "15m", "1h", "4h"]:
            htf_candles = tf_candles_dict.get(tf, [])
            ptr = mtf_pointers[tf]
            while ptr < len(htf_candles) and getattr(htf_candles[ptr], "close_time", 0) <= curr_close_time:
                candle_manager.update(htf_candles[ptr])
                mtf_manager.update_candle(htf_candles[ptr])
                ptr += 1
            mtf_pointers[tf] = ptr

        snapshot = builder.build("BTCUSDT", "1m")
        vec = fusion_engine.build_from_snapshot(snapshot)
        matrix.append(vec)

    matrix = np.array(matrix)
    print("Matrix shape:", matrix.shape)
    stds = np.std(matrix, axis=0)
    zero_count = 0
    for i, (name, s) in enumerate(zip(UNIFIED_FEATURE_SCHEMA, stds)):
        status = "OK" if s > 1e-8 else "CONSTANT (0)"
        if s <= 1e-8:
            zero_count += 1
        print(f"[{i:02d}] {name:<30} std={s:.8f} -> {status}")
    print(f"\nTotal Features: {len(UNIFIED_FEATURE_SCHEMA)} | Zero Variance: {zero_count} | Active Features: {len(UNIFIED_FEATURE_SCHEMA) - zero_count}")

if __name__ == "__main__":
    test_feature_variance()
