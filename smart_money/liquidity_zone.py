from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from enum import Enum


class LiquidityType(Enum):

    BUY_SIDE = "buy_side"

    SELL_SIDE = "sell_side"


class LiquidityStatus(Enum):

    ACTIVE = "active"

    SWEPT = "swept"

    INVALID = "invalid"


@dataclass(slots=True)
class LiquidityZone:

    symbol: str

    timeframe: str

    level: Decimal

    touches: int

    zone_type: LiquidityType

    created_at: int

    status: LiquidityStatus = LiquidityStatus.ACTIVE

    strength: float = 0.0