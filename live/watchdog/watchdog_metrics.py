from collections import defaultdict


class WatchdogMetrics:

    def __init__(self):

        self.success = defaultdict(int)

        self.failure = defaultdict(int)

    def healthy(
        self,
        component,
    ):

        self.success[
            component
        ] += 1

    def failed(
        self,
        component,
    ):

        self.failure[
            component
        ] += 1

    def statistics(self):

        return {

            "healthy": dict(
                self.success
            ),

            "failed": dict(
                self.failure
            ),

        }