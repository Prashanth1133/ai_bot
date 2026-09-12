from __future__ import annotations

UNIFIED_FEATURE_SCHEMA = [
    # ---------------------------------------------------------
    # 1. MARKET / OHLCV
    # ---------------------------------------------------------
    "close_price",
    "returns_5m",
    "volume_5m",
    "volatility_20m",

    # ---------------------------------------------------------
    # 2. MULTI TIMEFRAME
    # ---------------------------------------------------------
    "mtf_alignment_score",
    "tf_1m_trend_score",
    "tf_5m_trend_score",
    "tf_15m_trend_score",
    "tf_1h_trend_score",
    "tf_4h_trend_score",
    "tf_5m_rsi",
    "tf_15m_rsi",
    "tf_1h_rsi",

    # ---------------------------------------------------------
    # 3. SUPPORT / RESISTANCE
    # ---------------------------------------------------------
    "support_distance_pct",
    "resistance_distance_pct",
    "support_strength",
    "resistance_strength",
    "touch_count_support",
    "touch_count_resistance",
    "breakout_flag",
    "breakdown_flag",

    # ---------------------------------------------------------
    # 4. SMC
    # ---------------------------------------------------------
    "smc_atr",
    "smc_bos_flag",
    "smc_choch_flag",
    "smc_active_order_blocks",
    "smc_active_liquidity_zones",
    "smc_active_fvgs",

    # ---------------------------------------------------------
    # 5. CANDLE / PATTERNS
    # ---------------------------------------------------------
    "pattern_count",
    "primary_pattern_direction",
    "primary_pattern_strength",

    # ---------------------------------------------------------
    # 6. ORDER FLOW
    # ---------------------------------------------------------
    "orderflow_cvd",
    "orderflow_delta",
    "orderflow_buy_volume",
    "orderflow_sell_volume",
    "orderbook_imbalance",

    # ---------------------------------------------------------
    # 7. VOLUME PROFILE / VWAP
    # ---------------------------------------------------------
    "vp_poc_distance_pct",
    "vp_vah_distance_pct",
    "vp_val_distance_pct",
    "vwap_distance_pct",

    # ---------------------------------------------------------
    # 8. REGIME
    # ---------------------------------------------------------
    "regime_volatility",

    # ---------------------------------------------------------
    # 9. DERIVATIVES
    # ---------------------------------------------------------
    "derivatives_funding_rate",
    "derivatives_oi_change",
    "derivatives_taker_imbalance",

    # ---------------------------------------------------------
    # 10. NEWS
    # ---------------------------------------------------------
    "news_sentiment",
    "news_impact_score",
    "news_btc_relevance",

    # ---------------------------------------------------------
    # 11. ON-CHAIN
    # ---------------------------------------------------------
    "onchain_whale_score",
    "onchain_exchange_net_flow",
]

NUM_UNIFIED_FEATURES = 48

assert len(UNIFIED_FEATURE_SCHEMA) == NUM_UNIFIED_FEATURES

UNIFIED_FEATURE_NAMES = list(UNIFIED_FEATURE_SCHEMA)
