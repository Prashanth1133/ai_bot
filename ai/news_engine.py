import math


class NewsEngine:


    def __init__(self):

        self.news_score = 0.50

        self.label = "NEUTRAL"


    def evaluate(

        self,
        sentiment_score

    ):


        if sentiment_score > 0.75:

            self.news_score = 0.90

            self.label = "BULLISH"


        elif sentiment_score < 0.35:

            self.news_score = 0.10

            self.label = "BEARISH"


        else:

            self.news_score = 0.50

            self.label = "NEUTRAL"


        return {

            "score":self.news_score,

            "label":self.label

        }