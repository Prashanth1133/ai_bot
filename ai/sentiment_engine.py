class SentimentEngine:


    def __init__(self):

        self.score = 0.50


    def evaluate(

        self,
        bullish,
        bearish

    ):


        total = bullish + bearish


        if total == 0:

            return {

                "score":0.50

            }


        score = bullish/total


        self.score = round(

            score,

            4

        )


        return {

            "score":

            self.score

        }