from __future__ import annotations

from typing import Dict, List, Optional


class OrderRegistry:

    def __init__(self):

        self._orders: Dict[str, object] = {}

        self._symbol_index: Dict[str, List[str]] = {}

    def add(self, order):

        self._orders[order.order_id] = order

        self._symbol_index.setdefault(
            order.symbol,
            []
        ).append(order.order_id)

    def get(
        self,
        order_id: str,
    ):

        return self._orders.get(order_id)

    def exists(
        self,
        order_id: str,
    ) -> bool:

        return order_id in self._orders

    def remove(
        self,
        order_id: str,
    ):

        order = self._orders.pop(
            order_id,
            None,
        )

        if order is None:
            return

        ids = self._symbol_index.get(
            order.symbol,
            [],
        )

        if order_id in ids:
            ids.remove(order_id)

    def by_symbol(
        self,
        symbol: str,
    ):

        return [
            self._orders[i]
            for i in self._symbol_index.get(
                symbol,
                [],
            )
        ]

    def all(self):

        return list(self._orders.values())

    def clear(self):

        self._orders.clear()

        self._symbol_index.clear()