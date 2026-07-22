import numpy as np


class RegimeDetector:

    def detect(
        self,
        prices
    ):

        std = np.std(
            prices
        )

        if std < 100:
            return "SIDEWAYS"

        if prices[-1] > prices[0]:
            return "TRENDING_UP"

        return "TRENDING_DOWN"