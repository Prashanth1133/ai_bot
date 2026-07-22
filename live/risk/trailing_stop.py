from __future__ import annotations

from decimal import Decimal


class TrailingStop:

    def __init__(

        self,

        atr_multiplier: Decimal,

    ):

        self.multiplier = atr_multiplier

    def update(

        self,

        current_stop: Decimal,

        current_price: Decimal,

        atr: Decimal,

        long: bool,

    ):

        distance = atr * self.multiplier

        if long:

            candidate = current_price - distance

            return max(

                current_stop,

                candidate,

            )

        candidate = current_price + distance

        return min(

            current_stop,

            candidate,

        )