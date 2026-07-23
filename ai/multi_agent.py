class MultiAgentAI:


    def vote(

        self,
        decisions

    ):


        buy = 0

        sell = 0


        for decision in decisions:


            if "BUY" in decision:

                buy +=1


            elif "SELL" in decision:

                sell +=1


        if buy > sell:

            return "BUY"


        elif sell > buy:

            return "SELL"


        return "NO TRADE"