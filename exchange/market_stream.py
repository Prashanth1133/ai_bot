from __future__ import annotations

from exchange.stream_builder import (
    StreamBuilder,
)


class MarketStream:

    def __init__(self):

        self.streams = []

    def build(
        self,
        symbol: str,
        intervals=None,
    ):

        if intervals is None:
            intervals = [
                "1m",
                "5m",
                "15m",
            ]

        self.streams = [
            StreamBuilder.trade(symbol),
            StreamBuilder.depth(symbol),
            StreamBuilder.book_ticker(symbol),
            StreamBuilder.mark_price(symbol),
            StreamBuilder.liquidation(symbol),
        ]

        for tf in intervals:

            self.streams.append(
                StreamBuilder.kline(
                    symbol,
                    tf,
                )
            )

        return self.streams