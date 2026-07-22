from __future__ import annotations


class OrderStream:

    def __init__(self):

        self.orders = {}

    def update(
        self,
        payload,
    ):

        if payload.get("e") != "ORDER_TRADE_UPDATE":
            return

        order = payload["o"]

        self.orders[
            order["i"]
        ] = order

    def get(
        self,
        order_id,
    ):

        return self.orders.get(order_id)

    def all(self):

        return list(
            self.orders.values()
        )