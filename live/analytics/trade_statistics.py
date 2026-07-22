from __future__ import annotations

from decimal import Decimal


class TradeStatistics:

    def __init__(self):

        self.total = 0

        self.wins = 0

        self.losses = 0

        self.pnl = Decimal("0")

    ##########################################################

    def record(

        self,

        pnl,

    ):

        pnl = Decimal(str(pnl))

        self.total += 1

        self.pnl += pnl

        if pnl >= 0:

            self.wins += 1

        else:

            self.losses += 1

    ##########################################################

    @property
    def win_rate(self):

        if self.total == 0:

            return 0.0

        return self.wins / self.total

    ##########################################################

    @property
    def average_pnl(self):

        if self.total == 0:

            return Decimal("0")

        return self.pnl / Decimal(self.total)

    ##########################################################

    def summary(self):

        return {

            "trades": self.total,

            "wins": self.wins,

            "losses": self.losses,

            "win_rate": self.win_rate,

            "net_pnl": self.pnl,

            "average_pnl": self.average_pnl,

        }