from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class PerformanceSnapshot:

    equity: float

    unrealized_pnl: float

    realized_pnl: float

    drawdown: float

    timestamp: datetime