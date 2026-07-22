class VolatilityStrength:

    def calculate(

        self,

        atr,

        price

    ):

        ratio = atr / price

        return float(ratio)