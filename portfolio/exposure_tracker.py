from __future__ import annotations

from decimal import Decimal


class ExposureTracker:

    def __init__(self):

        self._values = {}

    def update(

        self,

        symbol: str,

        exposure: Decimal,

    ):

        self._values[symbol] = Decimal(
            str(exposure)
        )

    def total(self):

        return sum(
            self._values.values(),
            Decimal("0"),
        )

    def symbol(self, symbol: str):

        return self._values.get(
            symbol,
            Decimal("0"),
        )

    def clear(self):

        self._values.clear()