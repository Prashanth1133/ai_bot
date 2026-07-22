from collections import defaultdict


class StatisticMetrics:

    def __init__(self):

        self.updated = defaultdict(int)

    def record(self, name):

        self.updated[name] += 1

    def statistics(self):

        return dict(
            self.updated
        )