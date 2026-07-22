from __future__ import annotations


class ResourceMetrics:

    def __init__(self):

        self.samples = 0

        self.cpu_peak = 0.0

        self.memory_peak = 0.0

    def update(
        self,
        resource,
    ):

        self.samples += 1

        self.cpu_peak = max(
            self.cpu_peak,
            resource.cpu_percent,
        )

        self.memory_peak = max(
            self.memory_peak,
            resource.memory_mb,
        )