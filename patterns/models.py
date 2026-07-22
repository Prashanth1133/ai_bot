from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class PatternType(Enum):

    NONE = "none"

    BULLISH = "bullish"

    BEARISH = "bearish"


class PatternName(Enum):

    DOJI = "doji"

    HAMMER = "hammer"

    INVERTED_HAMMER = "inverted_hammer"

    SHOOTING_STAR = "shooting_star"

    ENGULFING_BULL = "bullish_engulfing"

    ENGULFING_BEAR = "bearish_engulfing"

    MORNING_STAR = "morning_star"

    EVENING_STAR = "evening_star"

    THREE_WHITE = "three_white_soldiers"

    THREE_BLACK = "three_black_crows"


@dataclass(slots=True)
class CandlePattern:

    pattern: PatternName

    direction: PatternType

    confidence: float

    candle_index: int