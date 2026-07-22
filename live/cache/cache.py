from __future__ import annotations

from live.cache.cache_entry import CacheEntry


class Cache:

    def __init__(self):

        self._entries = {}

    def put(

        self,

        key: str,

        value,

        ttl: float | None = None,

    ):

        self._entries[key] = CacheEntry(

            key=key,

            value=value,

            ttl=ttl,

        )

    def get(
        self,
        key: str,
    ):

        entry = self._entries.get(key)

        if entry is None:

            return None

        if entry.expired():

            self.remove(key)

            return None

        return entry.value

    def remove(
        self,
        key: str,
    ):

        self._entries.pop(key, None)

    def contains(
        self,
        key: str,
    ):

        return self.get(key) is not None

    def clear(self):

        self._entries.clear()