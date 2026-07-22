from __future__ import annotations

import asyncio


class QueueMonitor:

    def __init__(
        self,
        registry,
        interval=5,
    ):

        self.registry = registry

        self.interval = interval

        self.running = False

    async def start(self):

        self.running = True

        while self.running:

            for queue in self.registry.queues().values():

                queue.size()

            await asyncio.sleep(
                self.interval
            )

    def stop(self):

        self.running = False