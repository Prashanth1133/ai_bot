from collections import defaultdict


class PortfolioMetrics:

    def __init__(self):

        self.metrics = defaultdict(float)

    def update(

        self,

        key,

        value,

    ):

        self.metrics[key] = value

    def increment(

        self,

        key,

        value=1.0,

    ):

        self.metrics[key] += value

    def get(

        self,

        key,

        default=0.0,

    ):

        return self.metrics.get(key, default)

    def snapshot(self):

        return dict(self.metrics)