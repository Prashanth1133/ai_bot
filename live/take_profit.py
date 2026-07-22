class TakeProfit:

    def __init__(

        self,
        rr=2

    ):

        self.rr = rr

    def calculate(

        self,
        entry,
        stop

    ):

        risk = abs(

            entry - stop

        )

        return (

            entry +

            risk *

            self.rr

        )