from __future__ import annotations

from decimal import Decimal


class PaperPosition:

    def __init__(

        self,

        symbol,

    ):

        self.symbol = symbol

        self.quantity = Decimal("0")

        self.average_price = Decimal("0")

        self.realized_pnl = Decimal("0")

    ###########################################################

    def update(

        self,

        side,

        quantity,

        price,

    ):

        quantity = Decimal(str(quantity))

        price = Decimal(str(price))

        if side.upper() == "BUY":

            total = (

                self.average_price * self.quantity

            ) + (price * quantity)

            self.quantity += quantity

            self.average_price = (

                total / self.quantity

            )

        else:

            pnl = (

                price - self.average_price

            ) * quantity

            self.realized_pnl += pnl

            self.quantity -= quantity

            if self.quantity <= 0:

                self.quantity = Decimal("0")

                self.average_price = Decimal("0")

    ###########################################################

    @property

    def opened(self):

        return self.quantity > 0