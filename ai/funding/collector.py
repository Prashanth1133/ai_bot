import aiohttp
import asyncio


URL = (
    "https://fapi.binance.com"
    "/fapi/v1/fundingRate"
)


class FundingCollector:

    async def fetch(
        self,
        symbol
    ):

        params = {

            "symbol":
            symbol,

            "limit":
            100
        }

        async with (
            aiohttp.ClientSession()
            as session
        ):

            async with session.get(
                URL,
                params=params
            ) as resp:

                return (
                    await resp.json()
                )