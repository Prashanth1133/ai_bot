from __future__ import annotations

from decimal import Decimal


class ExchangeOrderBook:

    def __init__(self):

        self.symbol = ""

        self.bids = []

        self.asks = []

    ##################################################

    def update(

        self,

        symbol,

        bids,

        asks,

    ):

        self.symbol = symbol

        self.bids = sorted(

            bids,

            key=lambda x: x[0],

            reverse=True,

        )

        self.asks = sorted(

            asks,

            key=lambda x: x[0],

        )

    ##################################################

    @property
    def best_bid(self):

        if not self.bids:

            return Decimal("0")

        return self.bids[0][0]

    ##################################################

    @property
    def best_ask(self):

        if not self.asks:

            return Decimal("0")

        return self.asks[0][0]

    ##################################################

    @property
    def spread(self):

        if not self.bids or not self.asks:

            return Decimal("0")

        return self.best_ask - self.best_bid

    ##################################################

    @property
    def mid_price(self):

        if not self.bids or not self.asks:

            return Decimal("0")

        return (

            self.best_bid +

            self.best_ask

        ) / Decimal("2")