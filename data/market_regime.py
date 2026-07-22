import numpy as np


class MarketRegimeBuilder:

    def build(
        self,
        prices,
        window=50
    ):

        regimes = []

        for i in range(len(prices) - window):

            sma = np.mean(

                prices[
                    i:i + window
                ]

            )

            current = prices[i]

            ratio = current / sma

            if ratio > 1.05:
                regimes.append(0)

            elif ratio > 1.02:
                regimes.append(1)

            elif ratio > 1.00:
                regimes.append(2)

            elif ratio > 0.98:
                regimes.append(3)

            elif ratio > 0.95:
                regimes.append(4)

            else:
                regimes.append(5)

        return np.array(regimes)