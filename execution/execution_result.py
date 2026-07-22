from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from datetime import datetime


@dataclass(slots=True)
class ExecutionResult:

    success: bool

    order_id: str

    symbol: str

    side: str

    quantity: Decimal

    price: Decimal

    fee: Decimal

    message: str

    timestamp: datetime