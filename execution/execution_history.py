from __future__ import annotations

from collections import deque


class ExecutionHistory:

    def __init__(
        self,
        max_size: int = 10000,
    ):

        self.history = deque(maxlen=max_size)

    def append(
        self,
        execution,
    ):

        self.history.append(execution)

    def latest(self):

        if not self.history:
            return None

        return self.history[-1]

    def all(self):

        return list(self.history)

    def clear(self):

        self.history.clear()