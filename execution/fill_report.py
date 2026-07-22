from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal


@dataclass(slots=True)
class FillReport:

    order_id: str

    trade_id: str

    symbol: str

    side: str

    quantity: Decimal

    price: Decimal

    commission: Decimal

    liquidity: str

    timestamp: datetime = field(
        default_factory=datetime.utcnow
    )