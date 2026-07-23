import numpy as np


class ConfidenceEngine:


    def calculate(

        self,
        confidence,
        sentiment,
        news,
        whale

    ):


        value = (

            confidence+

            sentiment+

            news+

            whale

        )/4


        return round(

            value,

            4

        )