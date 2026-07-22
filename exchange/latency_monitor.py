from __future__ import annotations

import time


class ExchangeLatencyMonitor:

    def __init__(self):

        self.samples = []

    def record(
        self,
        started: float,
    ):

        self.samples.append(
            time.perf_counter() - started
        )

    @property
    def average(self):

        if not self.samples:
            return 0.0

        return (
            sum(self.samples)
            / len(self.samples)
        )

    @property
    def maximum(self):

        if not self.samples:
            return 0.0

        return max(self.samples)

    @property
    def minimum(self):

        if not self.samples:
            return 0.0

        return min(self.samples)