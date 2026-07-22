from __future__ import annotations

from collections import defaultdict


class EventMetrics:

    def __init__(self):

        self.events = defaultdict(int)

    def record(
        self,
        event_type: str,
    ):

        self.events[event_type] += 1

    def count(
        self,
        event_type: str,
    ):

        return self.events.get(
            event_type,
            0,
        )

    def all(self):

        return dict(self.events)