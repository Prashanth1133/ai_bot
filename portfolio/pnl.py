from __future__ import annotations

from decimal import Decimal
from typing import Dict


class PnLManager:

    def __init__(self):

        self._realized: Dict[str, Decimal] = {}
        self._unrealized: Dict[str, Decimal] = {}

    def update_realized(
        self,
        symbol: str,
        pnl: Decimal,
    ):

        self._realized[symbol] = pnl

    def update_unrealized(
        self,
        symbol: str,
        pnl: Decimal,
    ):

        self._unrealized[symbol] = pnl

    def realized(
        self,
        symbol: str,
    ):

        return self._realized.get(symbol, Decimal("0"))

    def unrealized(
        self,
        symbol: str,
    ):

        return self._unrealized.get(symbol, Decimal("0"))

    def total_realized(self):

        return sum(
            self._realized.values(),
            Decimal("0"),
        )

    def total_unrealized(self):

        return sum(
            self._unrealized.values(),
            Decimal("0"),
        )

    def total(self):

        return (
            self.total_realized()
            + self.total_unrealized()
        )

    def reset(self):

        self._realized.clear()
        self._unrealized.clear()