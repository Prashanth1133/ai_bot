from __future__ import annotations


class ReconciliationEngine:

    def compare(
        self,
        exchange_orders,
        local_orders,
    ):

        exchange = {
            o["order_id"]: o
            for o in exchange_orders
        }

        local = {
            o["order_id"]: o
            for o in local_orders
        }

        missing_local = [
            exchange[k]
            for k in exchange.keys() - local.keys()
        ]

        missing_exchange = [
            local[k]
            for k in local.keys() - exchange.keys()
        ]

        matched = [
            local[k]
            for k in local.keys() & exchange.keys()
        ]

        return {
            "matched": matched,
            "missing_local": missing_local,
            "missing_exchange": missing_exchange,
        }