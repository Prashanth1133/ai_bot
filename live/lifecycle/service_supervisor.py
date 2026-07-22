from __future__ import annotations

import asyncio


class ServiceSupervisor:

    def __init__(
        self,
        registry,
        interval=5,
    ):

        self.registry = registry

        self.interval = interval

    async def supervise(self):

        while True:

            for service in self.registry.services():

                healthy = await service.health()

                if not healthy:

                    await service.stop()

                    await asyncio.sleep(1)

                    await service.start()

            await asyncio.sleep(
                self.interval
            )