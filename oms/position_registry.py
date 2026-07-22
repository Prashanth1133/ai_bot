from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import Dict, Optional


@dataclass(slots=True)
class Position:

    symbol: str

    quantity: Decimal = Decimal("0")

    average_price: Decimal = Decimal("0")

    realized_pnl: Decimal = Decimal("0")

    unrealized_pnl: Decimal = Decimal("0")


class PositionRegistry:

    def __init__(self):

        self._positions: Dict[str, Position] = {}

    def get(
        self,
        symbol: str,
    ) -> Optional[Position]:

        return self._positions.get(symbol)

    def all(self):
        return list(self._positions.values())

    def update(
        self,
        symbol: str,
        quantity: Decimal,
        price: Decimal,
    ):

        position = self._positions.get(symbol)

        if position is None:

            position = Position(symbol=symbol)

            self._positions[symbol] = position

        total = position.quantity + quantity

        if total == 0:

            position.quantity = Decimal("0")

            position.average_price = Decimal("0")

            return

        if position.quantity == 0:

            position.average_price = price

            position.quantity = quantity

            return

        position.average_price = (
            (
                position.average_price * position.quantity
            )
            + (price * quantity)
        ) / total

        position.quantity = total

    def remove(
        self,
        symbol: str,
    ):
        self._positions.pop(symbol, None)

    def clear(self):
        self._positions.clear()