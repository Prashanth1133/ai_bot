from __future__ import annotations

from collections import OrderedDict


class ExecutionCache:

    def __init__(
        self,
        max_size: int = 5000,
    ):

        self.max_size = max_size

        self.cache = OrderedDict()

    def put(
        self,
        order_id,
        result,
    ):

        self.cache[order_id] = result

        self.cache.move_to_end(order_id)

        if len(self.cache) > self.max_size:

            self.cache.popitem(last=False)

    def get(
        self,
        order_id,
    ):

        if order_id not in self.cache:
            return None

        self.cache.move_to_end(order_id)

        return self.cache[order_id]

    def clear(self):

        self.cache.clear()