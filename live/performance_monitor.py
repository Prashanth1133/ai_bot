from __future__ import annotations

from datetime import datetime


class PerformanceMonitor:

    def __init__(self):

        self.total_trades = 0

        self.wins = 0

        self.losses = 0

        self.total_profit = 0.0

        self.total_loss = 0.0

        self.max_drawdown = 0.0

        self.current_equity = 0.0

        self.highest_equity = 0.0

        self.started = datetime.utcnow()

    ############################################################

    def record_trade(

        self,

        pnl,

    ):

        self.total_trades += 1

        if pnl >= 0:

            self.wins += 1

            self.total_profit += pnl

        else:

            self.losses += 1

            self.total_loss += abs(pnl)

    ############################################################

    def update_equity(

        self,

        equity,

    ):

        self.current_equity = equity

        self.highest_equity = max(

            self.highest_equity,

            equity,

        )

        if self.highest_equity > 0:

            drawdown = (

                self.highest_equity - equity

            ) / self.highest_equity

            self.max_drawdown = max(

                self.max_drawdown,

                drawdown,

            )

    ############################################################

    @property
    def win_rate(self):

        if self.total_trades == 0:

            return 0.0

        return self.wins / self.total_trades

    ############################################################

    @property
    def profit_factor(self):

        if self.total_loss == 0:

            return 999.0

        return self.total_profit / self.total_loss

    ############################################################

    def summary(self):

        return {

            "trades": self.total_trades,

            "wins": self.wins,

            "losses": self.losses,

            "win_rate": self.win_rate,

            "profit_factor": self.profit_factor,

            "drawdown": self.max_drawdown,

            "equity": self.current_equity,

            "running_since": self.started.isoformat(),

        }