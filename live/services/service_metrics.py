from collections import defaultdict


class ServiceMetrics:

    def __init__(self):

        self.started = defaultdict(int)

        self.stopped = defaultdict(int)

        self.failed = defaultdict(int)

    def record_started(self, service):

        self.started[service] += 1

    def record_stopped(self, service):

        self.stopped[service] += 1

    def record_failed(self, service):

        self.failed[service] += 1