import asyncio


class SessionMonitor:

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

            for session in self.registry.all():

                _ = session.state

            await asyncio.sleep(
                self.interval
            )

    def stop(self):

        self.running = False