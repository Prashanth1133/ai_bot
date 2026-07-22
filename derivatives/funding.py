from decimal import Decimal


class FundingAnalyzer:

    def analyze(self, funding_rate: Decimal):

        if funding_rate > Decimal("0.0005"):

            return "LONG_CROWDED"

        if funding_rate < Decimal("-0.0005"):

            return "SHORT_CROWDED"

        return "BALANCED"