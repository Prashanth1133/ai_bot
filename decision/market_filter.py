class MarketFilter:

    """
    Reject trades in poor market conditions.
    """

    def allow(

        self,

        signal,

    ):

        if signal.market_regime == "RANGING":

            return False

        if signal.news_impact == "EXTREME":

            return False

        return True