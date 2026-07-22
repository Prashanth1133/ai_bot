class LiquidationAnalyzer:

    def detect(

        self,

        long_liquidations,

        short_liquidations

    ):

        if long_liquidations > short_liquidations:

            return "LONGS_LIQUIDATED"

        if short_liquidations > long_liquidations:

            return "SHORTS_LIQUIDATED"

        return "BALANCED"