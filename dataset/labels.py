from dataclasses import dataclass
from enum import IntEnum


class MarketLabel(IntEnum):
    STRONG_BEARISH = 0
    BEARISH = 1
    NEUTRAL = 2
    BULLISH = 3
    STRONG_BULLISH = 4


class DirectionLabel(IntEnum):
    SELL = 0
    HOLD = 1
    BUY = 2


class RegimeLabel(IntEnum):
    BEAR = 0
    RANGE = 1
    BULL = 2


class ReversalLabel(IntEnum):
    NO_REVERSAL = 0
    REVERSAL = 1


@dataclass
class LabelConfig:
    horizon_15m: int = 15
    horizon_30m: int = 30
    horizon_1h: int = 60
    horizon_4h: int = 240
    min_direction_return: float = 0.0015
    buy_atr_multiplier: float = 1.0
    sell_atr_multiplier: float = 1.0
    min_regime_return: float = 0.005
    regime_atr_threshold: float = 3.0
    tp_atr_multiplier: float = 2.0
    sl_atr_multiplier: float = 1.0
    min_tp_pct: float = 0.002
    max_tp_pct: float = 0.08
    min_sl_pct: float = 0.001
    max_sl_pct: float = 0.04

    # Reversal config (tiered structural reversal)
    reversal_lookback_minutes: int = 60
    reversal_future_horizon_minutes: int = 60
    reversal_min_prior_move_atr: float = 1.0
    reversal_min_future_move_atr: float = 0.75
    reversal_min_directional_ratio: float = 0.55
    reversal_retrace_fraction: float = 0.30
    reversal_min_bars: int = 20