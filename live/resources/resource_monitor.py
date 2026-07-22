from __future__ import annotations

import asyncio

from live.resources.resource import Resource


class ResourceMonitor:

    def __init__(

        self,

        collector,

        registry,

        interval: float = 2.0,

    ):

        self.collector = collector

        self.registry = registry

        self.interval = interval

        self.running = False

    async def start(self):

        self.running = True

        while self.running:

            resources = self.collector.collect()

            for resource in resources:

                if isinstance(resource, Resource):

                    self.registry.update(
                        resource
                    )

            await asyncio.sleep(
                self.interval
            )

    def stop(self):

        self.running = False