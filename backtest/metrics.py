from __future__ import annotations

from decimal import Decimal


class PerformanceMetrics:

    def __init__(self):

        self.total_trades = 0

        self.winning_trades = 0

        self.losing_trades = 0

        self.total_return = Decimal("0")

        self.net_profit = Decimal("0")

        self.gross_profit = Decimal("0")

        self.gross_loss = Decimal("0")

        self.max_drawdown = Decimal("0")

        self.win_rate = Decimal("0")

        self.profit_factor = Decimal("0")

        self.expectancy = Decimal("0")

        self.sharpe = Decimal("0")

        self.sortino = Decimal("0")

        self.calmar = Decimal("0")

    def update(self, trade):

        self.total_trades += 1

        pnl = trade.realized_pnl

        self.net_profit += pnl

        if pnl > 0:

            self.winning_trades += 1

            self.gross_profit += pnl

        else:

            self.losing_trades += 1

            self.gross_loss += abs(pnl)

        if self.total_trades > 0:

            self.win_rate = Decimal(
                self.winning_trades
            ) / Decimal(self.total_trades)

        if self.gross_loss > 0:

            self.profit_factor = (
                self.gross_profit
                / self.gross_loss
            )