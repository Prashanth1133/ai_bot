from __future__ import annotations

import asyncio
from datetime import datetime, timedelta


class HeartbeatMonitor:

    def __init__(

        self,

        registry,

        timeout: float = 30.0,

        interval: float = 5.0,

    ):

        self.registry = registry

        self.timeout = timeout

        self.interval = interval

        self.running = False

    async def start(self):

        self.running = True

        while self.running:

            now = datetime.utcnow()

            for hb in self.registry.all():

                if (

                    now - hb.timestamp

                ) > timedelta(

                    seconds=self.timeout

                ):

                    hb.healthy = False

            await asyncio.sleep(
                self.interval
            )

    def stop(self):

        self.running = False