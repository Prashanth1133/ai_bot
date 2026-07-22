from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class OrderSnapshot:

    order_id: str

    symbol: str

    side: str

    status: str

    quantity: float

    executed_quantity: float

    average_price: float

    timestamp: datetime