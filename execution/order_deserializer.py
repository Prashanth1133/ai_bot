from __future__ import annotations


class OrderDeserializer:

    @staticmethod
    def deserialize(
        payload: dict,
        order_cls,
    ):

        return order_cls(

            symbol=payload["symbol"],

            side=payload["side"],

            order_type=payload["type"],

            quantity=payload["quantity"],

            price=payload.get("price"),

            stop_price=payload.get(
                "stop_price"
            ),

            client_order_id=payload.get(
                "client_order_id"
            ),
        )