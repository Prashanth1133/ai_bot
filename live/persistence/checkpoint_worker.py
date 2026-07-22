from __future__ import annotations

import asyncio


class CheckpointWorker:

    def __init__(
        self,
        manager,
        provider,
        interval: float,
    ):

        self.manager = manager

        self.provider = provider

        self.interval = interval

        self.running = False

    async def start(self):

        self.running = True

        while self.running:

            state = self.provider()

            self.manager.create(
                "autosave",
                state,
            )

            await asyncio.sleep(
                self.interval
            )

    def stop(self):

        self.running = False