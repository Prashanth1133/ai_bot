from __future__ import annotations


class TradeStream:

    def __init__(self):

        self.trades = []

    def update(
        self,
        payload,
    ):

        if payload.get("e") != "ORDER_TRADE_UPDATE":
            return

        order = payload["o"]

        if order["x"] != "TRADE":
            return

        self.trades.append(order)

    def latest(self):

        if not self.trades:
            return None

        return self.trades[-1]

    def history(self):

        return self.trades