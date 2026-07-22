from __future__ import annotations


class CheckpointMetrics:

    def __init__(self):

        self.created = 0

        self.loaded = 0

        self.failed = 0

    def record_created(self):

        self.created += 1

    def record_loaded(self):

        self.loaded += 1

    def record_failed(self):

        self.failed += 1