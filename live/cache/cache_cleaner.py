from __future__ import annotations

import asyncio


class CacheCleaner:

    def __init__(

        self,

        registry,

        interval: float = 60.0,

    ):

        self.registry = registry

        self.interval = interval

        self.running = False

    async def start(self):

        self.running = True

        while self.running:

            for cache in self.registry.caches().values():

                expired = []

                for key, entry in cache._entries.items():

                    if entry.expired():

                        expired.append(key)

                for key in expired:

                    cache.remove(key)

            await asyncio.sleep(
                self.interval
            )

    def stop(self):

        self.running = False