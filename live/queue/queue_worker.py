from __future__ import annotations

import asyncio


class QueueWorker:

    def __init__(
        self,
        queue,
        handler,
    ):

        self.queue = queue

        self.handler = handler

        self.running = False

    async def start(self):

        self.running = True

        while self.running:

            item = await self.queue.get()

            try:

                await self.handler(item)

            except Exception:

                pass

            await asyncio.sleep(0)

    def stop(self):

        self.running = False