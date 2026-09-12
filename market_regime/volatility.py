from __future__ import annotations


class VolatilityStrength:

    def calculate(
        self,
        atr,
        price,
    ) -> float:

        atr = float(atr)
        price = float(price)

        if not (atr == atr) or not (price == price):
            return 0.0

        if price <= 0.0:
            return 0.0

        if atr < 0.0:
            atr = 0.0

        return float(atr / price)