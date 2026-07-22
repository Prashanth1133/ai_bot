from __future__ import annotations

import asyncio


class RecoveryWorker:

    def __init__(
        self,
        manager,
        interval: float = 1.0,
    ):

        self.manager = manager

        self.interval = interval

        self.queue = asyncio.Queue()

        self.running = False

    async def submit(
        self,
        component,
    ):

        await self.queue.put(component)

    async def start(self):

        self.running = True

        while self.running:

            component = await self.queue.get()

            try:

                await self.manager.recover(component)

            finally:

                self.queue.task_done()

            await asyncio.sleep(self.interval)

    def stop(self):

        self.running = False