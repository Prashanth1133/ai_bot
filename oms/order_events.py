from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Any


@dataclass(slots=True)
class OrderEvent:

    order_id: str

    symbol: str

    event: str

    timestamp: datetime = field(
        default_factory=datetime.utcnow
    )

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )