from decimal import Decimal, ROUND_DOWN


class PrecisionManager:

    def round_price(
        self,
        price: Decimal,
        tick: Decimal,
    ):

        return (
            price.quantize(
                tick,
                rounding=ROUND_DOWN,
            )
        )

    def round_quantity(
        self,
        qty: Decimal,
        step: Decimal,
    ):

        return (
            qty.quantize(
                step,
                rounding=ROUND_DOWN,
            )
        )