from __future__ import annotations

from decimal import Decimal


class CommissionModel:

    """
    Exchange commission calculator.
    """

    def __init__(

        self,

        maker_fee=Decimal("0.0002"),

        taker_fee=Decimal("0.0004"),

    ):

        self.maker_fee = Decimal(maker_fee)

        self.taker_fee = Decimal(taker_fee)

    ##########################################################

    def calculate(

        self,

        price,

        quantity,

        maker=False,

    ):

        notional = Decimal(price) * Decimal(quantity)

        fee = self.maker_fee if maker else self.taker_fee

        return notional * fee

    ##########################################################

    def maker(

        self,

        price,

        quantity,

    ):

        return self.calculate(

            price,

            quantity,

            maker=True,

        )

    ##########################################################

    def taker(

        self,

        price,

        quantity,

    ):

        return self.calculate(

            price,

            quantity,

            maker=False,

        )