from __future__ import annotations

import asyncio
from datetime import datetime, timedelta


class TaskScheduler:

    def __init__(self):

        self.registry = None

        self.running = False

    def attach(
        self,
        registry,
    ):

        self.registry = registry

    async def start(self):

        self.running = True

        while self.running:

            now = datetime.utcnow()

            for task in self.registry.tasks():

                if not task.enabled:
                    continue

                if (
                    task.next_run is None
                    or now >= task.next_run
                ):

                    asyncio.create_task(
                        task.coroutine()
                    )

                    task.last_run = now

                    task.next_run = (
                        now
                        + timedelta(
                            seconds=task.interval
                        )
                    )

            await asyncio.sleep(0.1)

    def stop(self):

        self.running = False