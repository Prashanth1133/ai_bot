from __future__ import annotations

import requests
from decimal import Decimal

from app.logger import logger
from models.market import Candle


BINANCE_REST_URL = (
    "https://fapi.binance.com/fapi/v1/klines"
)


class BinanceHistoricalData:

    def __init__(self):

        self.url = BINANCE_REST_URL

    def fetch_klines(
        self,
        symbol: str,
        interval: str = "5m",
        limit: int = 150,
    ):

        params = {
            "symbol": symbol.upper(),
            "interval": interval,
            "limit": limit,
        }

        response = requests.get(
            self.url,
            params=params,
            timeout=15,
        )

        response.raise_for_status()

        data = response.json()

        candles = []

        for row in data:

            candle = self._convert(
                symbol,
                interval,
                row,
            )

            candles.append(candle)

        logger.success(
            f"[HISTORY] "
            f"{symbol.upper()} "
            f"{interval} "
            f"{len(candles)} candles loaded"
        )

        return candles

    @staticmethod
    def _convert(
        symbol: str,
        interval: str,
        row: list,
    ) -> Candle:

        return Candle(
            symbol=symbol.upper(),
            interval=interval,
            open_time=int(row[0]),
            close_time=int(row[6]) if len(row) > 6 else int(row[0]) + 300000,
            open=Decimal(str(row[1])),
            high=Decimal(str(row[2])),
            low=Decimal(str(row[3])),
            close=Decimal(str(row[4])),
            volume=Decimal(str(row[5])),
            trades=int(row[8]) if len(row) > 8 else 0,
            closed=True,
        )
