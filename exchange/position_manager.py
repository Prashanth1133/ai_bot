from __future__ import annotations

from decimal import Decimal

from exchange.models import ExchangePosition


class PositionManager:

    def __init__(self):

        self.positions: dict[str, ExchangePosition] = {}

    ########################################################

    def update(

        self,

        position: ExchangePosition,

    ):

        self.positions[position.symbol] = position

    ########################################################

    def remove(

        self,

        symbol: str,

    ):

        self.positions.pop(symbol, None)

    ########################################################

    def get(

        self,

        symbol: str,

    ):

        return self.positions.get(symbol)

    ########################################################

    def all(self):

        return list(self.positions.values())

    ########################################################

    @property
    def total_unrealized_pnl(self):

        return sum(

            p.unrealized_pnl

            for p in self.positions.values()

        )

    ########################################################

    @property
    def total_notional(self):

        return sum(

            abs(p.notional)

            for p in self.positions.values()

        )

    ########################################################

    @property
    def total_margin(self):

        return sum(

            p.initial_margin

            for p in self.positions.values()

        )