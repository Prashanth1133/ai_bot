from __future__ import annotations

import httpx

from app.settings import settings


class BinanceREST:
    """
    Async Binance Futures REST client.

    Used for:
    - Historical candle warm-up
    - Order-book snapshots
    """

    def __init__(self):
        self.client = httpx.AsyncClient(
            base_url=settings.BINANCE_REST,
            timeout=httpx.Timeout(
                connect=10.0,
                read=20.0,
                write=10.0,
                pool=10.0,
            ),
            limits=httpx.Limits(
                max_connections=10,
                max_keepalive_connections=5,
            ),
        )

    async def orderbook_snapshot(
        self,
        symbol: str,
        limit: int = 1000,
    ) -> dict:

        response = await self.client.get(
            "/fapi/v1/depth",
            params={
                "symbol": symbol.upper(),
                "limit": limit,
            },
        )

        response.raise_for_status()
        data = response.json()

        if isinstance(data, dict) and "lastUpdateId" in data:
            if data["lastUpdateId"] < 1_000_000:
                from app.logger import logger
                logger.warning(
                    f"Orderbook snapshot update ID {data['lastUpdateId']} for {symbol} is unusually low."
                )

        return data

    async def klines(
        self,
        symbol: str,
        interval: str,
        limit: int = 500,
    ) -> list:

        limit = max(1, min(int(limit), 1500))

        response = await self.client.get(
            "/fapi/v1/klines",
            params={
                "symbol": symbol.upper(),
                "interval": interval,
                "limit": limit,
            },
        )

        response.raise_for_status()

        return response.json()

    async def close(self):
        """
        Close the HTTP connection pool cleanly.
        """
        if not self.client.is_closed:
            await self.client.aclose()
