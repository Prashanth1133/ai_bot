from __future__ import annotations

import asyncio
import time


class Heartbeat:

    def __init__(
        self,
        interval: float = 30,
    ):

        self.interval = interval

        self.last = time.time()

    async def start(self):

        while True:

            self.last = time.time()

            await asyncio.sleep(self.interval)