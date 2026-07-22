from __future__ import annotations


class ExecutionRecovery:

    def __init__(self):

        self.pending = {}

    def register(
        self,
        order,
    ):

        self.pending[
            order.client_order_id
        ] = order

    def completed(
        self,
        client_order_id,
    ):

        self.pending.pop(
            client_order_id,
            None,
        )

    def outstanding(self):

        return list(
            self.pending.values()
        )