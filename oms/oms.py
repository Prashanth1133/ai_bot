from __future__ import annotations

from oms.order_registry import OrderRegistry
from oms.trade_registry import TradeRegistry
from oms.position_registry import PositionRegistry
from oms.fill_manager import FillManager
from oms.execution_tracker import ExecutionTracker


class OMS:

    def __init__(self):

        self.orders = OrderRegistry()

        self.trades = TradeRegistry()

        self.positions = PositionRegistry()

        self.fills = FillManager()

        self.execution = ExecutionTracker()

    def reset(self):

        self.orders.clear()

        self.trades.clear()

        self.positions.clear()