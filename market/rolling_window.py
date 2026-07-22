from collections import deque


class RollingWindow:

    def __init__(self, size=500):

        self.window = deque(maxlen=size)

    def add(self, candle):

        self.window.append(candle)

    def latest(self):

        if self.window:

            return self.window[-1]

        return None

    def previous(self):

        if len(self.window) < 2:

            return None

        return self.window[-2]

    def all(self):

        return list(self.window)

    def __len__(self):

        return len(self.window)