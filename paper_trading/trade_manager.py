# ==========================================
# paper_trading/trade_manager.py
# ==========================================

import time
from paper_trading.portfolio import PortfolioManager
from paper_trading.performance import PerformanceManager
from paper_trading.tracker import TradeTracker


class TradeManager:

    def __init__(self, portfolio=None, performance=None, tracker=None):

        self.portfolio = portfolio or PortfolioManager()

        self.performance = performance or PerformanceManager()

        self.tracker = tracker or TradeTracker()

        self.trades = []

    def open_position(self, signal):

        self.portfolio.open_position(
            signal
        )

        self.tracker.open(
            signal
        )

    def close_position(self, signal):

        trade = self.portfolio.close_position(
            signal
        )

        if trade is None:
            return None

        self.performance.record_trade(
            trade
        )

        self.tracker.close(
            trade
        )

        return trade

    def add_trade(
        self,
        symbol,
        action,
        price,
        quantity,
        pnl=0
    ):

        self.trades.append(
            {
                "time": time.time(),
                "symbol": symbol,
                "action": action,
                "price": price,
                "quantity": quantity,
                "pnl": pnl
            }
        )

    def all(self):

        return self.trades