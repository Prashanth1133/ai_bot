from decimal import Decimal


class CommissionManager:

    def __init__(
        self,
        maker=Decimal("0.0002"),
        taker=Decimal("0.0005"),
    ):

        self.maker = maker
        self.taker = taker

    def maker_fee(
        self,
        quantity,
        price,
    ):

        return (
            quantity
            * price
            * self.maker
        )

    def taker_fee(
        self,
        quantity,
        price,
    ):

        return (
            quantity
            * price
            * self.taker
        )