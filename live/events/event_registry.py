from __future__ import annotations


class EventRegistry:

    def __init__(self):

        self._events = {}

    def register(
        self,
        event,
    ):

        self._events[event.event_id] = event

    def get(
        self,
        event_id: str,
    ):

        return self._events.get(event_id)

    def remove(
        self,
        event_id: str,
    ):

        self._events.pop(event_id, None)

    def clear(self):

        self._events.clear()