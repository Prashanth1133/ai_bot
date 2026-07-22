from __future__ import annotations


class TradeLog:

    def __init__(self):

        self.trades = []

    def add(

        self,

        trade,

    ):

        self.trades.append(trade)

    def all(self):

        return self.trades

    def total(self):

        return len(self.trades)

    def winners(self):

        return [

            t

            for t in self.trades

            if t.realized_pnl > 0

        ]

    def losers(self):

        return [

            t

            for t in self.trades

            if t.realized_pnl <= 0

        ]