from __future__ import annotations


class TaskMetrics:

    def __init__(self):

        self.executed = 0

        self.failed = 0

        self.total_runtime = 0.0

    def update(
        self,
        runtime: float,
        success: bool,
    ):

        self.executed += 1

        self.total_runtime += runtime

        if not success:
            self.failed += 1

    @property
    def average_runtime(self):

        if self.executed == 0:
            return 0.0

        return (
            self.total_runtime
            / self.executed
        )