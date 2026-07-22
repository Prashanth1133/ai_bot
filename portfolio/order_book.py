from __future__ import annotations


class PortfolioOrderBook:

    def __init__(self):

        self._orders = {}

    def add(self, order):

        self._orders[
            order.order_id
        ] = order

    def get(
        self,
        order_id,
    ):

        return self._orders.get(
            order_id
        )

    def remove(
        self,
        order_id,
    ):

        self._orders.pop(
            order_id,
            None,
        )

    def all(self):

        return list(
            self._orders.values()
        )

    def clear(self):

        self._orders.clear()