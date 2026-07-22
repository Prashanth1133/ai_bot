from __future__ import annotations

from decimal import Decimal


class LocalOrderBook:

    def __init__(self, symbol: str):

        self.symbol = symbol

        self.last_update_id = 0

        self.bids = {}

        self.asks = {}

    def load_snapshot(self, snapshot):

        self.last_update_id = snapshot["lastUpdateId"]

        self.bids = {
            Decimal(price): Decimal(qty)
            for price, qty in snapshot["bids"]
        }

        self.asks = {
            Decimal(price): Decimal(qty)
            for price, qty in snapshot["asks"]
        }

    def apply(self, update):

        self.last_update_id = update["u"]

        for price, qty in update["b"]:

            p = Decimal(price)

            q = Decimal(qty)

            if q == 0:
                self.bids.pop(p, None)
            else:
                self.bids[p] = q

        for price, qty in update["a"]:

            p = Decimal(price)

            q = Decimal(qty)

            if q == 0:
                self.asks.pop(p, None)
            else:
                self.asks[p] = q