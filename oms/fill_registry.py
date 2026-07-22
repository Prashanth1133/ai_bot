from __future__ import annotations

from collections import defaultdict


class FillRegistry:

    def __init__(self):

        self._fills = defaultdict(list)

    def add(
        self,
        order_id: str,
        fill,
    ):

        self._fills[order_id].append(fill)

    def get(
        self,
        order_id: str,
    ):

        return list(self._fills.get(order_id, []))

    def remove(
        self,
        order_id: str,
    ):

        self._fills.pop(order_id, None)

    def clear(self):

        self._fills.clear()