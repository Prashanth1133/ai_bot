from __future__ import annotations

from collections import defaultdict


class ServiceMetrics:

    def __init__(self):

        self.starts = defaultdict(int)

        self.failures = defaultdict(int)

        self.restarts = defaultdict(int)

    def started(
        self,
        service,
    ):

        self.starts[service] += 1

    def failed(
        self,
        service,
    ):

        self.failures[service] += 1

    def restarted(
        self,
        service,
    ):

        self.restarts[service] += 1