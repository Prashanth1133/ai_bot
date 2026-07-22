class StrategySelector:

    """
    Future:

    Scalping

    Swing

    Breakout

    Mean Reversion

    Liquidity Grab

    Trend Following

    """

    def choose(

        self,

        regime,

    ):

        if regime == "TRENDING":

            return "TREND"

        return "MEAN_REVERSION"