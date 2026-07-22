from __future__ import annotations

from collections import deque
from datetime import datetime


class ExecutionAudit:

    def __init__(self, max_records: int = 100000):

        self._records = deque(maxlen=max_records)

    def record(
        self,
        order_id: str,
        event: str,
        details: dict | None = None,
    ):

        self._records.append(
            {
                "timestamp": datetime.utcnow(),
                "order_id": order_id,
                "event": event,
                "details": details or {},
            }
        )

    def history(self):

        return list(self._records)

    def latest(self):

        if not self._records:
            return None

        return self._records[-1]

    def clear(self):

        self._records.clear()