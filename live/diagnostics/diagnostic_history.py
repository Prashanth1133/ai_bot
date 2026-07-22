from __future__ import annotations

from collections import deque


class DiagnosticHistory:

    def __init__(
        self,
        size: int = 5000,
    ):

        self._history = deque(maxlen=size)

    def add(
        self,
        result,
    ):

        self._history.append(result)

    def latest(self):

        if not self._history:

            return None

        return self._history[-1]

    def all(self):

        return list(self._history)

    def clear(self):

        self._history.clear()