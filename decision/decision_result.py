from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from typing import Dict, Any


@dataclass(slots=True)
class DecisionResult:

    approved: bool

    action: str

    symbol: str

    confidence: float

    quantity: Decimal

    entry_price: Decimal | None = None

    stop_loss: Decimal | None = None

    take_profit: Decimal | None = None

    reason: str = ""

    metadata: Dict[str, Any] = field(default_factory=dict)

    timestamp: datetime = field(default_factory=datetime.utcnow)