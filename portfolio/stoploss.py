class ATRStopLoss:

    def calculate(

        self,

        entry,

        atr,

        multiplier=2

    ):

        return entry - atr * multiplier