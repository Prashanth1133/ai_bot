from __future__ import annotations


class CacheRegistry:

    def __init__(self):

        self._caches = {}

    def register(
        self,
        name: str,
        cache,
    ):

        self._caches[name] = cache

    def get(
        self,
        name: str,
    ):

        return self._caches.get(name)

    def remove(
        self,
        name: str,
    ):

        self._caches.pop(name, None)

    def caches(self):

        return dict(self._caches)

    def clear(self):

        self._caches.clear()