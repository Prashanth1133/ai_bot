from collections import deque


class ContextHistory:

    def __init__(

        self,

        size=5000,

    ):

        self._history = deque(maxlen=size)

    def add(self, snapshot):

        self._history.append(snapshot)

    def latest(self):

        if not self._history:

            return None

        return self._history[-1]

    def all(self):

        return list(self._history)