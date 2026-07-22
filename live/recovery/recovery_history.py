from __future__ import annotations

from collections import deque
from datetime import datetime


class RecoveryHistory:

    def __init__(
        self,
        size: int = 5000,
    ):

        self.records = deque(maxlen=size)

    def add(
        self,
        component,
        success,
        message="",
    ):

        self.records.append(
            {
                "component": component,
                "success": success,
                "message": message,
                "timestamp": datetime.utcnow(),
            }
        )

    def latest(self):

        if not self.records:

            return None

        return self.records[-1]

    def all(self):

        return list(self.records)