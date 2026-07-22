from __future__ import annotations

import asyncio


class ServiceManager:

    def __init__(self):

        self.services = {}

    def register(
        self,
        name,
        service,
    ):

        self.services[name] = service

    async def start_all(self):

        for service in self.services.values():

            await service.start()

    async def stop_all(self):

        for service in reversed(
            list(self.services.values())
        ):

            await service.stop()

    async def restart(
        self,
        name,
    ):

        service = self.services.get(name)

        if service is None:
            return

        await service.stop()

        await asyncio.sleep(1)

        await service.start()