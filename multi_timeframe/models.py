from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Trend(Enum):

    BULLISH = "bullish"
    BEARISH = "bearish"
    NEUTRAL = "neutral"


@dataclass(slots=True)
class TimeframeState:

    timeframe: str

    trend: Trend

    bos: bool

    choch: bool

    confidence: float