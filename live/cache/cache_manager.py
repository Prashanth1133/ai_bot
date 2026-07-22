from __future__ import annotations


class CacheManager:

    def __init__(self):

        self.registry = None

    def attach(
        self,
        registry,
    ):

        self.registry = registry

    def cache(
        self,
        name: str,
    ):

        return self.registry.get(name)

    def clear_all(self):

        for cache in self.registry.caches().values():

            cache.clear()