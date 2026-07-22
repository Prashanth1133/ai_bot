from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class ExecutionEvent:

    event: str

    order_id: str

    symbol: str

    timestamp: datetime = datetime.utcnow()