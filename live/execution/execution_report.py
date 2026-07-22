from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal


@dataclass(slots=True)
class ExecutionReport:

    success: bool

    order_id: str

    symbol: str

    side: str

    quantity: Decimal

    price: Decimal

    commission: Decimal

    exchange: str

    message: str