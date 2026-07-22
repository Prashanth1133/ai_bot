from __future__ import annotations

from decimal import Decimal


class PortfolioStatistics:

    def __init__(self):

        self.trades = 0
        self.wins = 0
        self.losses = 0

        self.gross_profit = Decimal("0")
        self.gross_loss = Decimal("0")

    def add_trade(
        self,
        pnl: Decimal,
    ):

        self.trades += 1

        if pnl >= 0:

            self.wins += 1
            self.gross_profit += pnl

        else:

            self.losses += 1
            self.gross_loss += abs(pnl)

    @property
    def win_rate(self):

        if self.trades == 0:
            return Decimal("0")

        return (
            Decimal(self.wins)
            / Decimal(self.trades)
        ) * Decimal("100")

    @property
    def profit_factor(self):

        if self.gross_loss == 0:
            return Decimal("0")

        return (
            self.gross_profit
            / self.gross_loss
        )

    def reset(self):

        self.__init__()