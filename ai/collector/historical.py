import os
import asyncio
import aiohttp
import pandas as pd
from datetime import datetime

BASE_URL = "https://fapi.binance.com"

SYMBOLS = [
    "BTCUSDT",
    "ETHUSDT",
    "DOGEUSDT",
]

INTERVALS = [
    "1m",
    "5m",
    "15m",
]

LIMIT = 1500


class HistoricalCollector:

    def __init__(self, storage="storage"):
        self.storage = storage
        os.makedirs(storage, exist_ok=True)

    async def fetch_klines(
        self,
        session,
        symbol,
        interval,
        start_time=None,
    ):

        params = {
            "symbol": symbol,
            "interval": interval,
            "limit": LIMIT,
        }

        if start_time:
            params["startTime"] = start_time

        async with session.get(
            f"{BASE_URL}/fapi/v1/klines",
            params=params
        ) as resp:

            return await resp.json()

    async def collect_symbol(
        self,
        symbol,
        interval
    ):

        path = f"{self.storage}/{symbol}"
        os.makedirs(path, exist_ok=True)

        all_rows = []

        async with aiohttp.ClientSession() as session:

            start = None

            while True:

                data = await self.fetch_klines(
                    session,
                    symbol,
                    interval,
                    start
                )

                if not data:
                    break

                all_rows.extend(data)

                if len(data) < LIMIT:
                    break

                start = data[-1][0] + 1

                await asyncio.sleep(0.2)

        df = pd.DataFrame(
            all_rows,
            columns=[
                "open_time",
                "open",
                "high",
                "low",
                "close",
                "volume",
                "close_time",
                "quote_volume",
                "trades",
                "taker_buy_volume",
                "taker_buy_quote",
                "ignore",
            ]
        )

        df.to_parquet(
            f"{path}/{interval}.parquet",
            index=False
        )

        print(
            f"{symbol} {interval} "
            f"{len(df)} rows saved."
        )


async def main():

    collector = HistoricalCollector()

    tasks = []

    for symbol in SYMBOLS:
        for interval in INTERVALS:

            tasks.append(
                collector.collect_symbol(
                    symbol,
                    interval
                )
            )

    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())