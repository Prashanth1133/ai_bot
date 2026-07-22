import numpy as np


class ReversalDetector:

    def build(
        self,
        prices,
        window=10
    ):

        labels = []

        for i in range(len(prices) - window):

            current = prices[i]

            future = prices[i + window]

            pct = (future - current) / current

            if abs(pct) > 0.02:
                labels.append(1)
            else:
                labels.append(0)

        return np.array(labels)