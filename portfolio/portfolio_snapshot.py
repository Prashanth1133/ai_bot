from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass(slots=True)
class PortfolioSnapshot:

    equity: float

    cash: float

    positions: dict = field(default_factory=dict)

    exposure: dict = field(default_factory=dict)

    pnl: dict = field(default_factory=dict)

    timestamp: datetime = field(
        default_factory=datetime.utcnow
    )