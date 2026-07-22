from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class OrderAck:

    order_id: str

    accepted: bool

    exchange: str

    timestamp: datetime

    reason: str = ""