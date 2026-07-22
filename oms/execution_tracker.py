from __future__ import annotations

from collections import defaultdict
from datetime import datetime


class ExecutionTracker:

    def __init__(self):

        self._events = defaultdict(list)

    def record(
        self,
        order_id: str,
        state: str,
        message: str = "",
    ):

        self._events[order_id].append(
            {
                "time": datetime.utcnow(),
                "state": state,
                "message": message,
            }
        )

    def history(
        self,
        order_id: str,
    ):
        return list(
            self._events.get(order_id, [])
        )

    def latest(
        self,
        order_id: str,
    ):

        events = self._events.get(order_id)

        if not events:
            return None

        return events[-1]

    def clear(
        self,
        order_id: str,
    ):
        self._events.pop(order_id, None)