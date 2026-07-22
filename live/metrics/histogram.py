from __future__ import annotations


class Histogram:

    def __init__(self):

        self.samples = []

    def observe(
        self,
        value: float,
    ):

        self.samples.append(value)

    def count(self):

        return len(self.samples)

    def minimum(self):

        if not self.samples:
            return 0.0

        return min(self.samples)

    def maximum(self):

        if not self.samples:
            return 0.0

        return max(self.samples)

    def average(self):

        if not self.samples:
            return 0.0

        return sum(self.samples) / len(self.samples)

    def clear(self):

        self.samples.clear()