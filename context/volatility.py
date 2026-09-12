from __future__ import annotations

from decimal import Decimal


class VolatilityAnalyzer:

    def analyze(self, atr, price):

        if not price or float(price) <= 0.0:
            return "LOW"

        if not atr or float(atr) <= 0.0:
            return "LOW"

        try:
            ratio = Decimal(str(atr)) / Decimal(str(price))

            if ratio > Decimal("0.015"):
                return "HIGH"

            if ratio > Decimal("0.007"):
                return "MEDIUM"

            return "LOW"
        except Exception:
            return "LOW"