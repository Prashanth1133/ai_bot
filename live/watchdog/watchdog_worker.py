from __future__ import annotations

import asyncio


class WatchdogWorker:

    def __init__(

        self,

        manager,

        interval: float = 5.0,

    ):

        self.manager = manager

        self.interval = interval

        self.running = False

    async def start(self):

        self.running = True

        while self.running:

            await self.manager.check()

            await asyncio.sleep(
                self.interval
            )

    def stop(self):

        self.running = False