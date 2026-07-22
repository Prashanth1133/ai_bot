from __future__ import annotations

from collections import deque


class LogBuffer:

    def __init__(

        self,

        size: int = 10000,

    ):

        self._buffer = deque(
            maxlen=size
        )

    def append(
        self,
        record,
    ):

        self._buffer.append(record)

    def latest(self):

        if not self._buffer:

            return None

        return self._buffer[-1]

    def records(self):

        return list(self._buffer)

    def clear(self):

        self._buffer.clear()