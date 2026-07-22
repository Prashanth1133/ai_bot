from collections import defaultdict


class JobMetrics:

    def __init__(self):

        self.executed = defaultdict(int)

        self.failed = defaultdict(int)

    def success(self, name):

        self.executed[name] += 1

    def failure(self, name):

        self.failed[name] += 1