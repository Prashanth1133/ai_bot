from __future__ import annotations

from decimal import Decimal


class TradeStatistics:

    def __init__(self):

        self.count = 0

        self.volume = Decimal("0")

        self.notional = Decimal("0")

        self.fees = Decimal("0")

    def update(
        self,
        quantity,
        price,
        commission,
    ):

        self.count += 1

        self.volume += quantity

        self.notional += quantity * price

        self.fees += commission

    @property
    def average_trade_size(self):

        if self.count == 0:
            return Decimal("0")

        return self.volume / self.count