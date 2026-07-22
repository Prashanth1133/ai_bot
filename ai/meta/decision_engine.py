class MetaDecisionEngine:

    def decide(
        self,
        orderflow,
        trend,
        news,
        risk
    ):

        score = (
            orderflow * 0.4
            + trend * 0.3
            + news * 0.2
            + risk * 0.1
        )

        if score > 0.8:
            return "BUY"

        if score < 0.3:
            return "SELL"

        return "HOLD"