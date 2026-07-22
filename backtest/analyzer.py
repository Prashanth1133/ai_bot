from __future__ import annotations

from collections import defaultdict
from decimal import Decimal


class StrategyAnalyzer:
    """
    Analyze completed trades and produce
    statistics for research.

    This class does NOT execute trades.

    It only studies them.
    """

    def __init__(self):

        self.trades = []

    ###########################################################

    def add_trade(self, trade):

        self.trades.append(trade)

    ###########################################################

    def total_trades(self):

        return len(self.trades)

    ###########################################################

    def winners(self):

        return [

            t

            for t in self.trades

            if t.realized_pnl > 0

        ]

    ###########################################################

    def losers(self):

        return [

            t

            for t in self.trades

            if t.realized_pnl <= 0

        ]

    ###########################################################

    def win_rate(self):

        total = len(self.trades)

        if total == 0:

            return Decimal("0")

        wins = len(self.winners())

        return Decimal(wins) / Decimal(total)

    ###########################################################

    def average_win(self):

        wins = self.winners()

        if not wins:

            return Decimal("0")

        return (

            sum(

                t.realized_pnl

                for t in wins

            )

            / Decimal(len(wins))

        )

    ###########################################################

    def average_loss(self):

        losses = self.losers()

        if not losses:

            return Decimal("0")

        return (

            sum(

                t.realized_pnl

                for t in losses

            )

            / Decimal(len(losses))

        )

    ###########################################################

    def grouped_by_symbol(self):

        groups = defaultdict(list)

        for trade in self.trades:

            groups[trade.symbol].append(trade)

        return groups

    ###########################################################

    def grouped_by_side(self):

        groups = defaultdict(list)

        for trade in self.trades:

            groups[trade.side].append(trade)

        return groups

    ###########################################################

    def grouped_by_regime(self):

        groups = defaultdict(list)

        for trade in self.trades:

            regime = getattr(

                trade,

                "market_regime",

                "UNKNOWN",

            )

            groups[regime].append(trade)

        return groups

    ###########################################################

    def grouped_by_pattern(self):

        groups = defaultdict(list)

        for trade in self.trades:

            pattern = getattr(

                trade,

                "pattern",

                "UNKNOWN",

            )

            groups[pattern].append(trade)

        return groups

    ###########################################################

    def grouped_by_news(self):

        groups = defaultdict(list)

        for trade in self.trades:

            news = getattr(

                trade,

                "news_label",

                "NONE",

            )

            groups[news].append(trade)

        return groups

    ###########################################################

    def grouped_by_session(self):

        groups = defaultdict(list)

        for trade in self.trades:

            session = getattr(

                trade,

                "session",

                "UNKNOWN",

            )

            groups[session].append(trade)

        return groups

    ###########################################################

    def grouped_by_confidence(self):

        buckets = {

            "LOW": [],

            "MEDIUM": [],

            "HIGH": [],

        }

        for trade in self.trades:

            confidence = getattr(

                trade,

                "confidence",

                0,

            )

            if confidence < 0.40:

                buckets["LOW"].append(trade)

            elif confidence < 0.75:

                buckets["MEDIUM"].append(trade)

            else:

                buckets["HIGH"].append(trade)

        return buckets

    ###########################################################

    def summary(self):

        return {

            "Trades": self.total_trades(),

            "WinRate": self.win_rate(),

            "AverageWin": self.average_win(),

            "AverageLoss": self.average_loss(),

            "Symbols": len(

                self.grouped_by_symbol()

            ),

            "Regimes": len(

                self.grouped_by_regime()

            ),

            "Patterns": len(

                self.grouped_by_pattern()

            ),

        }