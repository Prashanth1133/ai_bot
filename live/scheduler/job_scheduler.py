from __future__ import annotations

import asyncio
import time

from live.scheduler.job_result import JobResult


class JobScheduler:

    def __init__(self, registry, history=None):

        self.registry = registry

        self.history = history

        self.running = False

    async def start(self):

        self.running = True

        while self.running:

            now = time.time()

            for job in self.registry.jobs():

                if not job.enabled:

                    continue

                if job.next_run is None:

                    job.next_run = now

                if now >= job.next_run:

                    start = time.perf_counter()

                    success = True

                    message = ""

                    try:

                        result = job.callback()

                        if asyncio.iscoroutine(result):

                            await result

                    except Exception as exc:

                        success = False

                        message = str(exc)

                    duration = (
                        time.perf_counter() - start
                    )

                    if self.history:

                        self.history.add(

                            JobResult(

                                job_id=job.id,

                                success=success,

                                duration=duration,

                                message=message,

                            )

                        )

                    job.last_run = now

                    job.next_run = now + job.interval

            await asyncio.sleep(0.05)

    def stop(self):

        self.running = False