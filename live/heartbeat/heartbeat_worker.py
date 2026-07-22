from __future__ import annotations

import asyncio


class HeartbeatWorker:

    def __init__(

        self,

        manager,

        component: str,

        interval: float = 5.0,

    ):

        self.manager = manager

        self.component = component

        self.interval = interval

        self.running = False

    async def start(self):

        self.running = True

        while self.running:

            self.manager.beat(
                self.component
            )

            await asyncio.sleep(
                self.interval
            )

    def stop(self):

        self.running = False