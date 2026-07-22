from __future__ import annotations

from collections import deque
from datetime import datetime
from decimal import Decimal


class BalanceHistory:

    def __init__(self, max_history: int = 10000):

        self._history = deque(maxlen=max_history)

    def append(self, balance: Decimal):

        self._history.append(
            (
                datetime.utcnow(),
                Decimal(str(balance)),
            )
        )

    def latest(self):

        if not self._history:
            return None

        return self._history[-1]

    def history(self):

        return list(self._history)

    def clear(self):

        self._history.clear()