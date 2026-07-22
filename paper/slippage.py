from __future__ import annotations

from decimal import Decimal


class SlippageModel:

    def __init__(

        self,

        slippage_bps=Decimal("0.0005"),

    ):

        self.slippage = Decimal(slippage_bps)

    ##########################################################

    def apply(

        self,

        price,

        side,

        orderbook=None,

    ):

        price = Decimal(str(price))

        if side.upper() == "BUY":

            return price * (

                Decimal("1") + self.slippage

            )

        return price * (

            Decimal("1") - self.slippage

        )