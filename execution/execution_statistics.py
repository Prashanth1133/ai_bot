from __future__ import annotations

from decimal import Decimal


class ExecutionStatistics:

    def __init__(self):

        self.orders = 0

        self.filled = 0

        self.cancelled = 0

        self.rejected = 0

        self.total_fees = Decimal("0")

        self.total_slippage = Decimal("0")

    def record_fill(
        self,
        fee: Decimal,
        slippage: Decimal,
    ):

        self.orders += 1
        self.filled += 1

        self.total_fees += fee
        self.total_slippage += slippage

    def record_cancel(self):

        self.orders += 1
        self.cancelled += 1

    def record_reject(self):

        self.orders += 1
        self.rejected += 1