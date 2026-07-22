from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from decimal import Decimal
from typing import Dict

from models.market import Trade, TradeSide


@dataclass(slots=True)
class OrderFlowMetrics:
    """
    Stores cumulative order flow metrics for a symbol.
    """

    buy_volume: Decimal = Decimal("0")
    sell_volume: Decimal = Decimal("0")

    delta: Decimal = Decimal("0")
    cvd: Decimal = Decimal("0")

    trades: int = 0

    aggressive_buyers: int = 0
    aggressive_sellers: int = 0


class OrderFlowEngine:
    """
    Processes incoming trades and maintains
    cumulative order flow statistics.
    """

    def __init__(self, history_size: int = 5000):

        self.history_size = history_size

        self.metrics: Dict[str, OrderFlowMetrics] = {}

        self.trade_history: Dict[str, deque[Trade]] = {}

    def _ensure_symbol(self, symbol: str) -> None:
        """
        Initialize data structures for a symbol.
        """

        if symbol not in self.metrics:

            self.metrics[symbol] = OrderFlowMetrics()

            self.trade_history[symbol] = deque(
                maxlen=self.history_size
            )

    def process_trade(self, trade: Trade) -> OrderFlowMetrics:
        """
        Process one trade and update metrics.
        """

        self._ensure_symbol(trade.symbol)

        metrics = self.metrics[trade.symbol]

        qty = trade.quantity

        metrics.trades += 1

        if trade.side == TradeSide.BUY:

            metrics.buy_volume += qty

            metrics.delta += qty

            metrics.cvd += qty

            metrics.aggressive_buyers += 1

        else:

            metrics.sell_volume += qty

            metrics.delta -= qty

            metrics.cvd -= qty

            metrics.aggressive_sellers += 1

        self.trade_history[trade.symbol].append(trade)

        return metrics

    def get_metrics(self, symbol: str) -> OrderFlowMetrics:
        """
        Return current metrics for a symbol.
        """

        self._ensure_symbol(symbol)

        return self.metrics[symbol]

    def get_trade_history(self, symbol: str):
        """
        Return rolling trade history.
        """

        self._ensure_symbol(symbol)

        return list(self.trade_history[symbol])

    def reset_symbol(self, symbol: str):
        """
        Reset all metrics for one symbol.
        """

        self.metrics[symbol] = OrderFlowMetrics()

        self.trade_history[symbol] = deque(
            maxlen=self.history_size
        )