from __future__ import annotations


class OrderLookup:

    def __init__(self):

        self._client_to_exchange = {}

        self._exchange_to_client = {}

    def register(
        self,
        client_order_id: str,
        exchange_order_id: str,
    ):

        self._client_to_exchange[
            client_order_id
        ] = exchange_order_id

        self._exchange_to_client[
            exchange_order_id
        ] = client_order_id

    def client_id(
        self,
        exchange_order_id: str,
    ):

        return self._exchange_to_client.get(
            exchange_order_id
        )

    def exchange_id(
        self,
        client_order_id: str,
    ):

        return self._client_to_exchange.get(
            client_order_id
        )

    def clear(self):

        self._client_to_exchange.clear()

        self._exchange_to_client.clear()