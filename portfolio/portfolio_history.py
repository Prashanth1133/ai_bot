from collections import deque


class PortfolioHistory:

    def __init__(

        self,

        maxlen: int = 10000,

    ):

        self._history = deque(maxlen=maxlen)

    def append(self, snapshot):

        self._history.append(snapshot)

    def latest(self):

        if not self._history:

            return None

        return self._history[-1]

    def all(self):

        return list(self._history)

    def clear(self):

        self._history.clear()