from __future__ import annotations

import asyncio


class ServiceMonitor:

    def __init__(
        self,
        registry,
        interval: float = 5.0,
    ):

        self.registry = registry

        self.interval = interval

        self.running = False

    async def start(self):

        self.running = True

        while self.running:

            for service in self.registry.services():

                await service.health()

            await asyncio.sleep(
                self.interval
            )

    def stop(self):

        self.running = False