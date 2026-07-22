from __future__ import annotations

import asyncio
from collections import defaultdict


class LiveEventBus:

    def __init__(self):

        self._subscribers = defaultdict(list)

    def subscribe(
        self,
        event_type: str,
        callback,
    ):

        self._subscribers[event_type].append(
            callback
        )

    async def publish(
        self,
        event,
    ):

        callbacks = self._subscribers.get(
            event.event_type,
            [],
        )

        for callback in callbacks:

            asyncio.create_task(
                callback(event)
            )

    def clear(self):

        self._subscribers.clear()