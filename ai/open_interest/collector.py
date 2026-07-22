import aiohttp
import asyncio


URL = (
    "https://fapi.binance.com"
    "/fapi/v1/openInterest"
)


class OpenInterestCollector:

    async def fetch(
        self,
        symbol
    ):

        params = {
            "symbol":
            symbol
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