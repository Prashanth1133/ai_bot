from __future__ import annotations

from collections import OrderedDict


class OrderCache:

    def __init__(
        self,
        size=10000,
    ):

        self.size = size

        self.cache = OrderedDict()

    def put(
        self,
        order,
    ):

        self.cache[
            order.order_id
        ] = order

        self.cache.move_to_end(
            order.order_id
        )

        if len(self.cache) > self.size:

            self.cache.popitem(
                last=False,
            )

    def get(
        self,
        order_id,
    ):

        if order_id not in self.cache:
            return None

        self.cache.move_to_end(
            order_id
        )

        return self.cache[
            order_id
        ]

    def clear(self):

        self.cache.clear()