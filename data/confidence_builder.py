import numpy as np


class ConfidenceBuilder:

    def build(
        self,
        prices
    ):

        confidence = []

        for i in range(len(prices) - 1):

            move = abs(

                (prices[i + 1] - prices[i])

                / prices[i]

            )

            confidence.append(

                min(
                    move * 100,
                    1.0
                )

            )

        return np.array(confidence)