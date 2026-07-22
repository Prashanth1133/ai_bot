from __future__ import annotations


class OrderStatistics:

    def __init__(self):

        self.created = 0
        self.filled = 0
        self.cancelled = 0
        self.rejected = 0
        self.failed = 0

    def record_created(self):
        self.created += 1

    def record_filled(self):
        self.filled += 1

    def record_cancelled(self):
        self.cancelled += 1

    def record_rejected(self):
        self.rejected += 1

    def record_failed(self):
        self.failed += 1

    @property
    def total(self):

        return (
            self.created
            + self.filled
            + self.cancelled
            + self.rejected
            + self.failed
        )