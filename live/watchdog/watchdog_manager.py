from __future__ import annotations

import asyncio

from live.watchdog.watchdog_event import (
    WatchdogEvent,
)


class WatchdogManager:

    def __init__(self):

        self.registry = None

        self.history = None

    def attach_registry(
        self,
        registry,
    ):

        self.registry = registry

    def attach_history(
        self,
        history,
    ):

        self.history = history

    async def check(self):

        for component, callback in (

            self.registry.components().items()

        ):

            status = callback()

            if asyncio.iscoroutine(status):

                status = await status

            event = WatchdogEvent(

                component=component,

                status=(
                    "HEALTHY"

                    if status

                    else "FAILED"
                ),
            )

            if self.history:

                self.history.add(event)