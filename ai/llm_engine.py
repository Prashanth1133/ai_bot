class LLMEngine:


    def reasoning(

        self,
        data

    ):


        score = 0


        if data["news"] == "BULLISH":

            score += 1


        if data["whale"] == "BULLISH":

            score += 1


        if data["liquidation"] == "BULLISH":

            score += 1


        if data["options"] == "BULLISH":

            score += 1


        if data["signal"] == "BUY":

            score += 2


        if score >= 5:

            decision = "STRONG BUY"


        elif score >=3:

            decision = "BUY"


        elif score <=1:

            decision = "SELL"


        else:

            decision = "NO TRADE"


        return {

            "decision":

            decision,

            "score":

            score

        }