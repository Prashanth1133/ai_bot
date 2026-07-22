from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from typing import Dict, Any


@dataclass(slots=True)
class ExecutionContext:

    symbol: str

    side: str

    quantity: Decimal

    price: Decimal | None = None

    leverage: int = 1

    metadata: Dict[str, Any] = field(default_factory=dict)

    created_at: datetime = field(default_factory=datetime.utcnow)