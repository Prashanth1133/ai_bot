from __future__ import annotations


class TradeBook:

    def __init__(self):

        self._trades = {}

    def add(
        self,
        trade,
    ):

        self._trades[
            trade.trade_id
        ] = trade

    def get(
        self,
        trade_id,
    ):

        return self._trades.get(
            trade_id
        )

    def remove(
        self,
        trade_id,
    ):

        self._trades.pop(
            trade_id,
            None,
        )

    def all(self):

        return list(
            self._trades.values()
        )

    def clear(self):

        self._trades.clear()