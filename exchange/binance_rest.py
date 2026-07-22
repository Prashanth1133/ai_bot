from __future__ import annotations

from typing import Any, Dict, Optional

from exchange.rest_client import RestClient
from exchange.request_signer import RequestSigner
from exchange.timestamp_provider import TimestampProvider


class BinanceREST:

    def __init__(
        self,
        api_key: str,
        api_secret: str,
        testnet: bool = False,
    ):

        if testnet:
            base_url = "https://testnet.binancefuture.com"
        else:
            base_url = "https://fapi.binance.com"

        self.client = RestClient(base_url)

        self.signer = RequestSigner(api_secret)

        self.api_key = api_key

    def _headers(self):

        return {
            "X-MBX-APIKEY": self.api_key,
        }

    async def ping(self):

        return await self.client.get("/fapi/v1/ping")

    async def exchange_info(self):

        return await self.client.get("/fapi/v1/exchangeInfo")

    async def server_time(self):

        return await self.client.get("/fapi/v1/time")

    async def ticker(self, symbol: str):

        return await self.client.get(
            "/fapi/v1/ticker/price",
            params={"symbol": symbol},
        )

    async def orderbook(
        self,
        symbol: str,
        limit: int = 100,
    ):

        return await self.client.get(
            "/fapi/v1/depth",
            params={
                "symbol": symbol,
                "limit": limit,
            },
        )

    async def klines(
        self,
        symbol: str,
        interval: str,
        limit: int = 500,
    ):

        return await self.client.get(
            "/fapi/v1/klines",
            params={
                "symbol": symbol,
                "interval": interval,
                "limit": limit,
            },
        )