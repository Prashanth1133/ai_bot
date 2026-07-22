import time


class DecisionMonitor:

    def __init__(self):

        self.count = 0

        self.started = time.time()

    def record(self):

        self.count += 1

    @property
    def decisions_per_second(self):

        elapsed = time.time() - self.started

        if elapsed <= 0:
            return 0

        return self.count / elapsed