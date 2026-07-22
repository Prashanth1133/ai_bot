from __future__ import annotations

from collections import deque


class AuditHistory:

    def __init__(
        self,
        size: int = 100000,
    ):

        self._history = deque(
            maxlen=size
        )

    def add(
        self,
        record,
    ):

        self._history.append(record)

    def latest(self):

        if not self._history:

            return None

        return self._history[-1]

    def all(self):

        return list(self._history)

    def clear(self):

        self._history.clear()