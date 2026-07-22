
from enum import Enum


class Feature(str, Enum):

    # --------------------------------------------------
    # Price
    # --------------------------------------------------

    LAST_PRICE = "last_price"
    MID_PRICE = "mid_price"
    SPREAD = "spread"

    OPEN = "open"
    HIGH = "high"
    LOW = "low"
    CLOSE = "close"
    VOLUME = "volume"

    # --------------------------------------------------
    # Order Flow
    # --------------------------------------------------

    BUY_VOLUME = "buy_volume"
    SELL_VOLUME = "sell_volume"

    DELTA = "delta"
    CVD = "cvd"

    # --------------------------------------------------
    # Order Book
    # --------------------------------------------------

    BID_VOLUME = "bid_volume"
    ASK_VOLUME = "ask_volume"

    IMBALANCE = "imbalance"

    # --------------------------------------------------
    # Indicators
    # --------------------------------------------------

    EMA20 = "ema20"
    EMA50 = "ema50"
    EMA200 = "ema200"

    ATR = "atr"
    RSI = "rsi"
    MACD = "macd"

    VWAP = "vwap"

    VOLATILITY = "volatility"

    # --------------------------------------------------
    # Trend
    # --------------------------------------------------

    TREND = "trend"

    MARKET_TREND = "market_trend"

    TREND_SCORE = "trend_score"

    # --------------------------------------------------
    # Smart Money Concepts
    # --------------------------------------------------

    BOS = "bos"
    CHOCH = "choch"

    SWING_HIGH = "swing_high"
    SWING_LOW = "swing_low"

    BOS_SIGNAL = "bos_signal"
    CHOCH_SIGNAL = "choch_signal"

    ORDER_BLOCK = "order_block"

    ORDER_BLOCK_COUNT = "order_block_count"

    BULLISH_ORDER_BLOCK = "bullish_order_block"
    BEARISH_ORDER_BLOCK = "bearish_order_block"

    MITIGATED_BLOCKS = "mitigated_blocks"

    FVG = "fair_value_gap"

    BULLISH_FVG = "bullish_fvg"
    BEARISH_FVG = "bearish_fvg"

    OPEN_FVG_COUNT = "open_fvg_count"

    FVG_SCORE = "fvg_score"

    # --------------------------------------------------
    # Liquidity
    # --------------------------------------------------

    BUY_SIDE_LIQUIDITY = "buy_side_liquidity"
    SELL_SIDE_LIQUIDITY = "sell_side_liquidity"

    LIQUIDITY_SWEEP = "liquidity_sweep"

    LIQUIDITY_SCORE = "liquidity_score"

    # --------------------------------------------------
    # Patterns
    # --------------------------------------------------

    BULLISH_PATTERN = "bullish_pattern"
    BEARISH_PATTERN = "bearish_pattern"

    PATTERN_CONFIDENCE = "pattern_confidence"

    DOJI = "doji"
    HAMMER = "hammer"
    ENGULFING = "engulfing"

    THREE_WHITE = "three_white_soldiers"
    THREE_BLACK = "three_black_crows"

    # --------------------------------------------------
    # Structure
    # --------------------------------------------------

    HH = "hh"
    HL = "hl"
    LH = "lh"
    LL = "ll"

    # --------------------------------------------------
    # Volume Profile
    # --------------------------------------------------

    POC = "poc"
    VAH = "vah"
    VAL = "val"

    HVN = "high_volume_node"
    LVN = "low_volume_node"

    VOLUME_PROFILE_SCORE = "volume_profile_score"

    # --------------------------------------------------
    # Multi Timeframe
    # --------------------------------------------------

    HTF_TREND = "htf_trend"

    MTF_ALIGNMENT = "mtf_alignment"

    TIMEFRAME_SCORE = "timeframe_score"

    HTF_BOS = "htf_bos"
    HTF_CHOCH = "htf_choch"

    # --------------------------------------------------
    # Derivatives
    # --------------------------------------------------

    OPEN_INTEREST = "open_interest"

    OPEN_INTEREST_TREND = "open_interest_trend"

    FUNDING_RATE = "funding_rate"

    FUNDING_BIAS = "funding_bias"

    LONG_SHORT_RATIO = "long_short_ratio"

    TAKER_IMBALANCE = "taker_imbalance"

    LONG_LIQUIDATIONS = "long_liquidations"
    SHORT_LIQUIDATIONS = "short_liquidations"

    LIQUIDATION_SIGNAL = "liquidation_signal"

    # --------------------------------------------------
    # Market Regime
    # --------------------------------------------------

    MARKET_REGIME = "market_regime"

    REGIME_CONFIDENCE = "regime_confidence"

    TREND_STRENGTH = "trend_strength"

    VOLATILITY_STRENGTH = "volatility_strength"

    MOMENTUM_STRENGTH = "momentum_strength"

    # --------------------------------------------------
    # Context
    # --------------------------------------------------

    SESSION = "session"

    MARKET_CONTEXT_SCORE = "market_context_score"

    VOLATILITY_LEVEL = "volatility_level"


FEATURE_LIST = [feature.value for feature in Feature]

