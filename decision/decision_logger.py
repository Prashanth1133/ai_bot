from __future__ import annotations

from collections import deque


class DecisionLogger:

    def __init__(
        self,
        max_records: int = 5000,
    ):

        self.records = deque(maxlen=max_records)

    def record(
        self,
        decision,
    ):

        self.records.append(decision)

    def latest(self):

        if not self.records:
            return None

        return self.records[-1]

    def history(self):

        return list(self.records)

    def clear(self):

        self.records.clear()