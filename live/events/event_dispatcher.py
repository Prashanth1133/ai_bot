from __future__ import annotations


class EventDispatcher:

    def __init__(
        self,
        event_bus,
        event_filter=None,
    ):

        self.event_bus = event_bus

        self.event_filter = event_filter

    async def dispatch(
        self,
        event,
    ):

        if self.event_filter:

            if not self.event_filter.accepts(
                event
            ):
                return

        await self.event_bus.publish(
            event
        )