import numpy as np


class SignalFusion:


    def calculate(

        self,
        transformer_score,
        news_score,
        sentiment_score,
        social_score,
        whale_score,
        confidence_score

    ):


        score = (

            transformer_score*0.40 +

            news_score*0.10 +

            sentiment_score*0.10 +

            social_score*0.10 +

            whale_score*0.10 +

            confidence_score*0.20

        )


        return round(

            score,

            4

        )


    def decision(

        self,
        score

    ):


        if score >= 0.90:

            return "STRONG BUY"


        if score >=0.75:

            return "BUY"


        if score <=0.30:

            return "SELL"


        return "NO TRADE"