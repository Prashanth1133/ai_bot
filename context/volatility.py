from decimal import Decimal


class VolatilityAnalyzer:

    def analyze(self, atr, price):

        ratio = atr / price

        if ratio > Decimal("0.015"):

            return "HIGH"

        if ratio > Decimal("0.007"):

            return "MEDIUM"

        return "LOW"