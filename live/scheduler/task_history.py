from __future__ import annotations

from collections import deque
from datetime import datetime


class TaskHistory:

    def __init__(self):

        self.records = deque(maxlen=10000)

    def add(
        self,
        task,
        success: bool,
        runtime: float,
    ):

        self.records.append(
            {
                "task": task,
                "success": success,
                "runtime": runtime,
                "time": datetime.utcnow(),
            }
        )

    def latest(self):

        if not self.records:
            return None

        return self.records[-1]

    def all(self):

        return list(self.records)