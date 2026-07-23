class LiquidationEngine:


    def evaluate(

        self,
        long_liquidation,
        short_liquidation

    ):


        if long_liquidation > short_liquidation:

            signal = "BEARISH"


        elif short_liquidation > long_liquidation:

            signal = "BULLISH"


        else:

            signal = "NEUTRAL"


        return {

            "signal":

            signal

        }