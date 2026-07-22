from __future__ import annotations

import asyncio
import time


class RateLimiter:

    def __init__(
        self,
        requests: int,
        seconds: float,
    ):

        self.requests = requests
        self.seconds = seconds

        self.calls = []

    async def acquire(self):

        while True:

            now = time.monotonic()

            self.calls = [
                t
                for t in self.calls
                if now - t < self.seconds
            ]

            if len(self.calls) < self.requests:

                self.calls.append(now)

                return

            await asyncio.sleep(0.05)