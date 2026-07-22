from dataclasses import dataclass
from decimal import Decimal
from enum import Enum


class OrderBlockType(Enum):

    BULLISH = "bullish"

    BEARISH = "bearish"


class OrderBlockStatus(Enum):

    ACTIVE = "active"

    MITIGATED = "mitigated"

    INVALID = "invalid"


@dataclass(slots=True)
class OrderBlock:

    symbol: str

    timeframe: str

    type: OrderBlockType

    high: Decimal

    low: Decimal

    created_at: int

    strength: float

    status: OrderBlockStatus = OrderBlockStatus.ACTIVE