
from enum import Enum
from dataclasses import dataclass
from typing import Optional


class Trend(Enum):
    UNKNOWN = 0
    BULLISH = 1
    BEARISH = -1
    RANGING = 2


@dataclass
class MarketState:
    """
    Represents the current Smart Money market state.
    """

    trend: Trend = Trend.UNKNOWN

    last_hh: Optional[float] = None
    last_hl: Optional[float] = None
    last_lh: Optional[float] = None
    last_ll: Optional[float] = None

    bos: bool = False
    choch: bool = False

