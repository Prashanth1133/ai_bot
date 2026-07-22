from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal


@dataclass(slots=True)
class EquityPoint:

    timestamp: datetime

    equity: Decimal

class EquityCurve:

    def __init__(self, max_points: int = 100000):

        self._points = deque(maxlen=max_points)

    def append(
        self,
        equity: Decimal,
    ):

        self._points.append(
            EquityPoint(
                timestamp=datetime.utcnow(),
                equity=equity,
            )
        )

    def latest(self):

        if not self._points:
            return None

        return self._points[-1]

    def all(self):

        return list(self._points)

    def clear(self):

        self._points.clear()