from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass(slots=True)
class ContextSnapshot:

    symbol: str

    timeframe: str

    timestamp: datetime = field(
        default_factory=datetime.utcnow
    )

    market: dict = field(default_factory=dict)

    orderflow: dict = field(default_factory=dict)

    indicators: dict = field(default_factory=dict)

    smart_money: dict = field(default_factory=dict)

    sentiment: dict = field(default_factory=dict)

    derivatives: dict = field(default_factory=dict)

    onchain: dict = field(default_factory=dict)

    news: dict = field(default_factory=dict)

    regime: dict = field(default_factory=dict)

    metadata: dict = field(default_factory=dict)