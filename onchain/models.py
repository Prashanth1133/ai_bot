from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class OnChainEvent:

    timestamp: datetime

    blockchain: str

    tx_hash: str

    from_address: str

    to_address: str

    asset: str

    amount: float

    usd_value: float

    exchange: str | None = None

    event_type: str = ""

    confidence: float = 0.0