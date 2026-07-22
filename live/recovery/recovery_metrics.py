from collections import defaultdict


class RecoveryMetrics:

    def __init__(self):

        self.success = defaultdict(int)

        self.failure = defaultdict(int)

    def record_success(
        self,
        component,
    ):

        self.success[component] += 1

    def record_failure(
        self,
        component,
    ):

        self.failure[component] += 1

    def statistics(self):

        return {

            "success": dict(self.success),

            "failure": dict(self.failure),
        }