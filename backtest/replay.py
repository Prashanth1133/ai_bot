from __future__ import annotations

import asyncio


class ReplayEngine:

    """
    Replays historical candles as websocket
    kline messages into the MarketEngine.
    """

    async def replay(

        self,

        dataframe,

        market_engine,

    ):

        for row in dataframe.itertuples(index=False):

            message = {

                "stream": f"{row.symbol.lower()}@kline_1m",

                "data": {

                    "e": "kline",

                    "E": int(row.timestamp),

                    "s": row.symbol,

                    "k": {

                        "t": int(row.timestamp),

                        "T": int(row.timestamp),

                        "s": row.symbol,

                        "i": "1m",

                        "o": str(row.open),

                        "c": str(row.close),

                        "h": str(row.high),

                        "l": str(row.low),

                        "v": str(row.volume),

                        "x": True,

                    },

                },

            }

            await market_engine.handler(message)

            await asyncio.sleep(0)