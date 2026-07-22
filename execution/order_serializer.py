from __future__ import annotations


class OrderSerializer:

    @staticmethod
    def serialize(order):

        return {

            "symbol": order.symbol,

            "side": order.side,

            "type": order.order_type,

            "quantity": str(order.quantity),

            "price": (
                None
                if order.price is None
                else str(order.price)
            ),

            "stop_price": (
                None
                if order.stop_price is None
                else str(order.stop_price)
            ),

            "client_order_id": order.client_order_id,
        }