from __future__ import annotations

from exchange.models import ExchangeOrder


class OrderManager:

    def __init__(self):

        self.orders: dict[str, ExchangeOrder] = {}

    ########################################################

    def add(

        self,

        order: ExchangeOrder,

    ):

        self.orders[order.order_id] = order

    ########################################################

    def remove(

        self,

        order_id: str,

    ):

        self.orders.pop(order_id, None)

    ########################################################

    def get(

        self,

        order_id: str,

    ):

        return self.orders.get(order_id)

    ########################################################

    def by_symbol(

        self,

        symbol: str,

    ):

        return [

            order

            for order in self.orders.values()

            if order.symbol == symbol

        ]

    ########################################################

    def open_orders(self):

        return [

            order

            for order in self.orders.values()

            if order.status in (

                "NEW",

                "PARTIALLY_FILLED",

            )

        ]

    ########################################################

    def filled_orders(self):

        return [

            order

            for order in self.orders.values()

            if order.status == "FILLED"

        ]

    ########################################################

    def cancelled_orders(self):

        return [

            order

            for order in self.orders.values()

            if order.status == "CANCELED"

        ]

    ########################################################

    def clear(self):

        self.orders.clear()