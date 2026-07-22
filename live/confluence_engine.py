class ConfluenceEngine:

    def score(

        self,

        ai,

        smc,

        orderflow,

        orderbook,

        news,

    ):

        score = 0

        if ai:
            score += 35

        if smc:
            score += 20

        if orderflow:
            score += 15

        if orderbook:
            score += 15

        if news:
            score += 15

        return score