from __future__ import annotations

from decimal import Decimal


class AccountStatistics:

    def __init__(self):

        self.balance = Decimal("0")

        self.equity = Decimal("0")

        self.margin = Decimal("0")

        self.free_margin = Decimal("0")

        self.margin_level = Decimal("0")

    def update(

        self,

        balance,

        equity,

        margin,

        free_margin,

    ):

        self.balance = Decimal(str(balance))

        self.equity = Decimal(str(equity))

        self.margin = Decimal(str(margin))

        self.free_margin = Decimal(str(free_margin))

        if self.margin > 0:

            self.margin_level = (

                self.equity

                / self.margin

            ) * Decimal("100")