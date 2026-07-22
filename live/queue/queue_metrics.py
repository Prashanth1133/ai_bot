from __future__ import annotations


class QueueMetrics:

    def __init__(self):

        self.enqueued = 0

        self.dequeued = 0

        self.failed = 0

    def record_enqueue(self):

        self.enqueued += 1

    def record_dequeue(self):

        self.dequeued += 1

    def record_failure(self):

        self.failed += 1

    @property
    def pending(self):

        return self.enqueued - self.dequeued