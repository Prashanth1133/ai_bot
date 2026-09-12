from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from enum import Enum


from typing import Any


class FVGType(Enum):

    BULLISH = "bullish"

    BEARISH = "bearish"


class FVGStatus(Enum):

    OPEN = "open"

    FILLED = "filled"

    INVALID = "invalid"


@dataclass(slots=True)
class FairValueGap:

    symbol: str

    timeframe: str

    gap_type: FVGType

    upper: Decimal

    lower: Decimal

    created_at: int

    strength: float

    status: FVGStatus = FVGStatus.OPEN

    open_time: int | None = None

    candle: Any = None