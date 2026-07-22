from __future__ import annotations


class PaperStatistics:

    def __init__(self):

        self.trades = 0

        self.pnl = 0

    ###########################################################

    def update(

        self,

        fill,

    ):

        self.trades += 1

        self.pnl += fill.get(

            "realized_pnl",

            0,

        )

    ###########################################################

    def summary(self):

        return {

            "trades": self.trades,

            "realized_pnl": self.pnl,

        }