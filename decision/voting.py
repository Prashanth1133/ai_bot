class VotingEngine:

    """
    Majority voting from all engines.
    """

    def vote(

        self,

        signal,

    ):

        votes = [

            signal.ai_direction,

            signal.smart_money_direction,

            signal.orderflow_direction,

            signal.news_direction,

        ]

        bullish = votes.count("BUY")

        bearish = votes.count("SELL")

        if bullish > bearish:

            return "BUY"

        if bearish > bullish:

            return "SELL"

        return "HOLD"