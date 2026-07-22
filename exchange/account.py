from __future__ import annotations

from decimal import Decimal

from exchange.models import ExchangeBalance
from exchange.models import ExchangePosition


class ExchangeAccount:

    def __init__(self):

        self._balances: dict[str, ExchangeBalance] = {}

        self._positions: dict[str, ExchangePosition] = {}

    ########################################################

    def update_balance(

        self,

        balance: ExchangeBalance,

    ):

        self._balances[balance.asset] = balance

    ########################################################

    def update_position(

        self,

        position: ExchangePosition,

    ):

        self._positions[position.symbol] = position

    ########################################################

    def balance(

        self,

        asset: str,

    ):

        return self._balances.get(asset)

    ########################################################

    def position(

        self,

        symbol: str,

    ):

        return self._positions.get(symbol)

    ########################################################

    def balances(self):

        return list(self._balances.values())

    ########################################################

    def positions(self):

        return list(self._positions.values())

    ########################################################

    @property
    def wallet_balance(self):

        return sum(

            b.wallet_balance

            for b in self._balances.values()

        )

    ########################################################

    @property
    def available_balance(self):

        return sum(

            b.available_balance

            for b in self._balances.values()

        )

    ########################################################

    @property
    def unrealized_pnl(self):

        return sum(

            p.unrealized_pnl

            for p in self._positions.values()

        )

    ########################################################

    @property
    def equity(self):

        return self.wallet_balance + self.unrealized_pnl