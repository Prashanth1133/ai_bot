from __future__ import annotations


class CacheMetrics:

    def __init__(self):

        self.hits = 0

        self.misses = 0

        self.evictions = 0

    def hit(self):

        self.hits += 1

    def miss(self):

        self.misses += 1

    def eviction(self):

        self.evictions += 1

    @property
    def hit_rate(self):

        total = self.hits + self.misses

        if total == 0:

            return 0.0

        return self.hits / total