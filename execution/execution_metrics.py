from __future__ import annotations

from collections import defaultdict
from decimal import Decimal


class ExecutionMetrics:

    def __init__(self):

        self.total_orders = 0
        self.successful_orders = 0
        self.failed_orders = 0

        self.total_volume = Decimal("0")

        self.total_notional = Decimal("0")

        self.symbol_metrics = defaultdict(
            lambda: {
                "orders": 0,
                "volume": Decimal("0"),
                "notional": Decimal("0"),
            }
        )

    def record(
        self,
        symbol: str,
        quantity: Decimal,
        price: Decimal,
        success: bool,
    ):

        self.total_orders += 1

        if success:
            self.successful_orders += 1
        else:
            self.failed_orders += 1

        self.total_volume += quantity
        self.total_notional += quantity * price

        metric = self.symbol_metrics[symbol]

        metric["orders"] += 1
        metric["volume"] += quantity
        metric["notional"] += quantity * price

    @property
    def success_rate(self):

        if self.total_orders == 0:
            return 0.0

        return self.successful_orders / self.total_orders