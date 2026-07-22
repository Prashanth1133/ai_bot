from __future__ import annotations


class OrderTracker:

    def __init__(self):

        self.orders = {}

    def add(
        self,
        order,
    ):

        self.orders[
            order["orderId"]
        ] = order

    def update(
        self,
        order,
    ):

        self.orders[
            order["orderId"]
        ] = order

    def remove(
        self,
        order_id,
    ):

        self.orders.pop(
            order_id,
            None,
        )

    def get(
        self,
        order_id,
    ):

        return self.orders.get(
            order_id
        )

    def all(self):

        return list(
            self.orders.values()
        )