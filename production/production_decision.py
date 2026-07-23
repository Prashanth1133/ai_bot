class ProductionDecision:


    def decide(

        self,
        signal,
        confidence,
        regime

    ):


        if confidence < 0.75:

            return "SKIP"


        if regime == "SIDEWAYS":

            return "SKIP"


        if signal == "BUY":

            return "EXECUTE BUY"


        if signal == "SELL":

            return "EXECUTE SELL"


        return "NO TRADE"