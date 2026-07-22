import aiohttp
import asyncio


URL = (
    "https://fapi.binance.com"
    "/futures/data/"
    "allForceOrders"
)


class LiquidationCollector:

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


async def main():

    data = (
        await
        LiquidationCollector()
        .fetch(
            "BTCUSDT"
        )
    )

    print(
        len(data)
    )


if __name__ == "__main__":
    asyncio.run(main())