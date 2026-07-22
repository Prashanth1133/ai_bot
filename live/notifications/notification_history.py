from __future__ import annotations

from collections import deque


class NotificationHistory:

    def __init__(
        self,
        size: int = 10000,
    ):

        self._history = deque(
            maxlen=size
        )

    def add(
        self,
        notification,
    ):

        self._history.append(notification)

    def latest(self):

        if not self._history:

            return None

        return self._history[-1]

    def all(self):

        return list(self._history)

    def clear(self):

        self._history.clear()