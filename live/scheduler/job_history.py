from collections import deque


class JobHistory:

    def __init__(self, size: int = 10000):

        self._history = deque(maxlen=size)

    def add(self, result):

        self._history.append(result)

    def latest(self):

        if not self._history:

            return None

        return self._history[-1]

    def all(self):

        return list(self._history)