from decimal import Decimal


class ATRPositionSizer:

    def __init__(

        self,

        risk_percent: Decimal,

        atr_multiplier: Decimal,

    ):

        self.risk = risk_percent

        self.multiplier = atr_multiplier

    def calculate(

        self,

        equity: Decimal,

        atr: Decimal,

    ):

        risk_amount = (

            equity

            * self.risk

        )

        stop_distance = (

            atr

            * self.multiplier

        )

        return (

            risk_amount

            / stop_distance

        )