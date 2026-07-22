class PositionSizer:

    def __init__(

        self,
        risk_percent=1.0

    ):

        self.risk_percent = (

            risk_percent / 100

        )

    def calculate(

        self,
        balance,
        entry,
        stop_loss

    ):

        risk_amount = (

            balance *

            self.risk_percent

        )

        risk_per_unit = abs(

            entry - stop_loss

        )

        if risk_per_unit == 0:

            return 0

        quantity = (

            risk_amount /

            risk_per_unit

        )

        return quantity