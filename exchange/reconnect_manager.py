from __future__ import annotations

import asyncio


class ReconnectManager:

    def __init__(
        self,
        max_attempts=0,
        delay=5,
    ):

        self.max_attempts = max_attempts
        self.delay = delay

    async def wait(
        self,
        attempt: int,
    ):

        if (
            self.max_attempts
            and attempt > self.max_attempts
        ):
            raise RuntimeError(
                "Maximum reconnect attempts exceeded."
            )

        await asyncio.sleep(self.delay)