from collections import defaultdict


class DiagnosticMetrics:

    def __init__(self):

        self.success = defaultdict(int)

        self.failure = defaultdict(int)

    def record(
        self,
        result,
    ):

        if result.passed:

            self.success[
                result.component
            ] += 1

        else:

            self.failure[
                result.component
            ] += 1

    def statistics(self):

        return {

            "success": dict(
                self.success
            ),

            "failure": dict(
                self.failure
            ),

        }