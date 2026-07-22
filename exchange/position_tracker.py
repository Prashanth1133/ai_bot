from __future__ import annotations

from decimal import Decimal


class PositionTracker:

    def __init__(self):

        self.positions = {}

    def update(
        self,
        symbol,
        qty,
        entry,
        pnl,
    ):

        self.positions[symbol] = {

            "qty": Decimal(str(qty)),

            "entry": Decimal(str(entry)),

            "pnl": Decimal(str(pnl)),
        }

    def get(
        self,
        symbol,
    ):

        return self.positions.get(symbol)

    def remove(
        self,
        symbol,
    ):

        self.positions.pop(
            symbol,
            None,
        )

    def all(self):

        return self.positions