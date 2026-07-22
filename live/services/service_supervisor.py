import asyncio


class ServiceSupervisor:

    def __init__(self, registry):

        self.registry = registry

        self.running = False

    async def start(self):

        self.running = True

        while self.running:

            for service in self.registry.all():

                _ = service.state

            await asyncio.sleep(1.0)

    def stop(self):

        self.running = False