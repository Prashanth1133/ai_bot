from __future__ import annotations

from collections import defaultdict
from smart_money.order_block_types import OrderBlockStatus


class OrderBlockManager:
    """
    Manages Order Blocks with deduplication and bounded history.
    """

    def __init__(self, max_blocks_per_symbol: int = 500):
        self.max_blocks_per_symbol = int(max_blocks_per_symbol)
        self.blocks = defaultdict(list)
        self._known = defaultdict(set)

    @staticmethod
    def _block_key(block):
        symbol = str(getattr(block, "symbol", "")).upper()
        created_at = getattr(block, "created_at", None)
        high = round(float(getattr(block, "high", 0.0)), 8)
        low = round(float(getattr(block, "low", 0.0)), 8)
        block_type = str(getattr(block, "type", ""))
        return (symbol, created_at, high, low, block_type)

    def add(self, block):
        if block is None:
            return False

        symbol = str(getattr(block, "symbol", "")).upper()
        if not symbol:
            return False

        key = self._block_key(block)
        if key in self._known[symbol]:
            return False

        self.blocks[symbol].append(block)
        self._known[symbol].add(key)

        if len(self.blocks[symbol]) > self.max_blocks_per_symbol:
            removed = self.blocks[symbol][: len(self.blocks[symbol]) - self.max_blocks_per_symbol]
            self.blocks[symbol] = self.blocks[symbol][-self.max_blocks_per_symbol :]
            for old_b in removed:
                self._known[symbol].discard(self._block_key(old_b))

        return True

    def add_many(self, blocks):
        added = 0
        for block in blocks or []:
            if self.add(block):
                added += 1
        return added

    def active(self, symbol):
        symbol = str(symbol).upper()
        return [
            b
            for b in self.blocks.get(symbol, [])
            if getattr(b, "status", None) == OrderBlockStatus.ACTIVE
            or getattr(getattr(b, "status", None), "name", str(getattr(b, "status", ""))) == "ACTIVE"
        ]

    def update(self, symbol, price):
        symbol = str(symbol).upper()
        price = float(price)
        if price <= 0:
            return

        for block in self.blocks.get(symbol, []):
            status = getattr(block, "status", None)
            status_name = getattr(status, "name", str(status))
            if status_name != "ACTIVE":
                continue

            low = float(getattr(block, "low", 0.0))
            high = float(getattr(block, "high", 0.0))
            if low <= price <= high:
                block.status = OrderBlockStatus.MITIGATED

    def reset(self):
        self.blocks.clear()
        self._known.clear()