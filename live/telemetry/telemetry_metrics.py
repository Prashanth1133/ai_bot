from collections import defaultdict


class TelemetryMetrics:

    def __init__(self):

        self.samples = defaultdict(int)

    def record(

        self,

        component,

    ):

        self.samples[
            component
        ] += 1

    def statistics(self):

        return dict(
            self.samples
        )