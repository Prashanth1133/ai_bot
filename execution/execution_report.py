from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from typing import List


@dataclass(slots=True)
class ExecutionReport:

    symbol: str

    side: str

    requested_qty: Decimal

    filled_qty: Decimal

    average_price: Decimal

    commission: Decimal

    slippage: Decimal

    status: str

    order_ids: List[str] = field(default_factory=list)

    timestamp: datetime = field(default_factory=datetime.utcnow)