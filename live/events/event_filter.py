from __future__ import annotations


class EventFilter:

    def __init__(self):

        self.allowed = set()

    def allow(
        self,
        event_type: str,
    ):

        self.allowed.add(event_type)

    def accepts(
        self,
        event,
    ):

        if not self.allowed:

            return True

        return (
            event.event_type
            in self.allowed
        )