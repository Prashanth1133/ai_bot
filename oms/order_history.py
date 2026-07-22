from __future__ import annotations

from collections import defaultdict


class OrderHistory:

    def __init__(self):

        self._history = defaultdict(list)

    def add(
        self,
        order_id,
        event,
    ):

        self._history[
            order_id
        ].append(event)

    def history(
        self,
        order_id,
    ):

        return self._history.get(
            order_id,
            [],
        )

    def clear(
        self,
        order_id,
    ):

        self._history.pop(
            order_id,
            None,
        )