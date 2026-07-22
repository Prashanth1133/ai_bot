from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class TradeSnapshot:

    trade_id: str

    order_id: str

    symbol: str

    side: str

    quantity: float

    price: float

    fee: float

    timestamp: datetime