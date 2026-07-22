from collections import deque


class LifecycleHistory:

    def __init__(

        self,

        size: int = 10000,

    ):

        self._history = deque(
            maxlen=size
        )

    def add(
        self,
        event,
    ):

        self._history.append(event)

    def latest(self):

        if not self._history:

            return None

        return self._history[-1]

    def all(self):

        return list(self._history)

    def clear(self):

        self._history.clear()