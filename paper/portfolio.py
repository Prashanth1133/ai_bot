from __future__ import annotations

from paper.position import PaperPosition


class PaperPortfolio:

    def __init__(

        self,

        balance=10000,

    ):

        self.balance = float(balance)

        self.positions = {}

    ###########################################################

    def process_fill(

        self,

        fill,

    ):

        symbol = fill["symbol"]

        if symbol not in self.positions:

            self.positions[symbol] = PaperPosition(

                symbol

            )

        position = self.positions[symbol]

        position.update(

            fill["side"],

            fill["quantity"],

            fill["price"],

        )

        self.balance -= fill["commission"]

    ###########################################################

    def snapshot(self):

        return {

            "balance": self.balance,

            "positions": self.positions,

        }