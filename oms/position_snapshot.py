from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class PositionSnapshot:

    symbol: str

    quantity: float

    entry_price: float

    mark_price: float

    unrealized_pnl: float

    timestamp: datetime