class ConfidenceCalculator:

    """
    Calculates confidence from weighted features.
    """

    WEIGHTS = {

        "bos": 15,

        "choch": 15,

        "order_block": 15,

        "liquidity": 15,

        "trend": 15,

        "orderflow": 10,

        "volume": 10,

        "candlestick": 5
    }

    def calculate(self, features):

        score = 0

        total = sum(self.WEIGHTS.values())

        for feature, weight in self.WEIGHTS.items():

            if features.get(feature):

                score += weight

        return round((score / total) * 100, 2)