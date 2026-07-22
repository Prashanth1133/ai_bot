from decimal import Decimal


class TakerVolumeAnalyzer:

    def imbalance(

        self,

        buy: Decimal,

        sell: Decimal

    ):

        total = buy + sell

        if total == 0:

            return Decimal("0")

        return (buy - sell) / total