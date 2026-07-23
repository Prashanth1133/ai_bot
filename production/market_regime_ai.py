class MarketRegimeAI:


    def predict(

        self,
        volatility,
        trend_score

    ):


        if trend_score > 0.80:

            return "TRENDING"


        if volatility > 0.70:

            return "HIGH VOLATILITY"


        if volatility < 0.20:

            return "SIDEWAYS"


        return "RANGING"