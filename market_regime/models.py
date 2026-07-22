from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class MarketRegime(Enum):

    STRONG_UPTREND = "strong_uptrend"

    WEAK_UPTREND = "weak_uptrend"

    STRONG_DOWNTREND = "strong_downtrend"

    WEAK_DOWNTREND = "weak_downtrend"

    ACCUMULATION = "accumulation"

    DISTRIBUTION = "distribution"

    RANGE = "range"

    BREAKOUT = "breakout"

    REVERSAL = "reversal"

    HIGH_VOLATILITY = "high_volatility"

    LOW_VOLATILITY = "low_volatility"


@dataclass(slots=True)
class RegimeState:

    regime: MarketRegime

    confidence: float

    score: float