from __future__ import annotations

from collections import defaultdict
from smart_money.liquidity_zone import LiquidityStatus


class LiquidityManager:
    """
    Manages Liquidity Zones with deduplication and bounded history.
    """

    def __init__(self, max_zones_per_symbol: int = 500):
        self.max_zones_per_symbol = int(max_zones_per_symbol)
        self.zones = defaultdict(list)
        self._known = defaultdict(set)

    @staticmethod
    def _zone_key(zone):
        symbol = str(getattr(zone, "symbol", "")).upper()
        created_at = getattr(zone, "created_at", None)
        level = round(float(getattr(zone, "level", 0.0)), 8)
        zone_type = str(getattr(zone, "zone_type", ""))
        return (symbol, created_at, level, zone_type)

    def add(self, zone):
        if zone is None:
            return False

        symbol = str(getattr(zone, "symbol", "")).upper()
        if not symbol:
            return False

        key = self._zone_key(zone)
        if key in self._known[symbol]:
            return False

        self.zones[symbol].append(zone)
        self._known[symbol].add(key)

        if len(self.zones[symbol]) > self.max_zones_per_symbol:
            removed = self.zones[symbol][: len(self.zones[symbol]) - self.max_zones_per_symbol]
            self.zones[symbol] = self.zones[symbol][-self.max_zones_per_symbol :]
            for old_z in removed:
                self._known[symbol].discard(self._zone_key(old_z))

        return True

    def add_many(self, zones):
        added = 0
        for zone in zones or []:
            if self.add(zone):
                added += 1
        return added

    def active(self, symbol):
        symbol = str(symbol).upper()
        return [
            z
            for z in self.zones.get(symbol, [])
            if getattr(z, "status", None) == LiquidityStatus.ACTIVE
            or getattr(getattr(z, "status", None), "name", str(getattr(z, "status", ""))) == "ACTIVE"
        ]

    def update(self, symbol, price):
        symbol = str(symbol).upper()
        price = float(price)
        if price <= 0:
            return

        for zone in self.zones.get(symbol, []):
            status = getattr(zone, "status", None)
            status_name = getattr(status, "name", str(status))
            if status_name != "ACTIVE":
                continue

            level = float(getattr(zone, "level", 0.0))
            if level > 0 and abs(price - level) / level < 0.001:
                zone.status = LiquidityStatus.SWEPT

    def reset(self):
        self.zones.clear()
        self._known.clear()