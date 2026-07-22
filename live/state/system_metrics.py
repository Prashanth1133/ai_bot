from __future__ import annotations


class SystemMetrics:

    def __init__(self):

        self.starts = 0

        self.stops = 0

        self.restarts = 0

        self.failures = 0

    def record_start(self):

        self.starts += 1

    def record_stop(self):

        self.stops += 1

    def record_restart(self):

        self.restarts += 1

    def record_failure(self):

        self.failures += 1

    def reset(self):

        self.starts = 0
        self.stops = 0
        self.restarts = 0
        self.failures = 0