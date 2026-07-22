import numpy as np


class VolatilityBuilder:

    def build(
        self,
        prices,
        window=20
    ):

        values = []

        returns = np.diff(prices) / prices[:-1]

        for i in range(len(returns) - window):

            values.append(

                np.std(
                    returns[i:i + window]
                )

            )

        return np.array(values)