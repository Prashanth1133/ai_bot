from collections import defaultdict


class LogMetrics:

    def __init__(self):

        self.levels = defaultdict(int)

    def update(
        self,
        level,
    ):

        self.levels[level] += 1

    def count(
        self,
        level,
    ):

        return self.levels[level]

    def statistics(self):

        return dict(self.levels)