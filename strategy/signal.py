from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass(slots=True)
class StrategySignal:

    symbol: str

    action: str

    confidence: float

    price: float

    timeframe: str

    strategy: str

    metadata: dict = field(default_factory=dict)

    timestamp: datetime = field(
        default_factory=datetime.utcnow
    )