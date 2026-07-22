from __future__ import annotations

import httpx

from app.settings import settings


class BinanceREST:

    def __init__(self):

        self.client = httpx.AsyncClient(
            base_url=settings.BINANCE_REST,
            timeout=10
        )

    async def orderbook_snapshot(
        self,
        symbol: str,
        limit: int = 1000
    ):

        response = await self.client.get(
            "/fapi/v1/depth",
            params={
                "symbol": symbol.upper(),
                "limit": limit
            }
        )

        response.raise_for_status()

        return response.json()