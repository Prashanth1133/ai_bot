class TrendStrength:

    def calculate(

        self,

        ema20,

        ema50,

        ema200

    ):

        if ema20 > ema50 > ema200:

            return 1.0

        if ema20 > ema50:

            return 0.7

        if ema20 < ema50 < ema200:

            return -1.0

        if ema20 < ema50:

            return -0.7

        return 0.0