from __future__ import annotations

from decimal import Decimal


class PerformanceTracker:

    def __init__(self):

        self.gross_profit = Decimal("0")

        self.gross_loss = Decimal("0")

        self.net_profit = Decimal("0")

    def record_trade(
        self,
        pnl,
    ):

        pnl = Decimal(str(pnl))

        self.net_profit += pnl

        if pnl >= 0:

            self.gross_profit += pnl

        else:

            self.gross_loss += abs(pnl)

    @property
    def profit_factor(self):

        if self.gross_loss == 0:

            return Decimal("0")

        return (

            self.gross_profit

            / self.gross_loss

        )