from __future__ import annotations

import aiohttp

from exchange.rest_response import RestResponse


class RestClient:

    def __init__(
        self,
        base_url: str,
        timeout: int = 10,
    ):

        self.base_url = base_url.rstrip("/")

        self.timeout = aiohttp.ClientTimeout(
            total=timeout,
        )

    async def get(
        self,
        endpoint: str,
        **kwargs,
    ):

        async with aiohttp.ClientSession(
            timeout=self.timeout,
        ) as session:

            async with session.get(
                self.base_url + endpoint,
                **kwargs,
            ) as response:

                data = await response.json()

                return RestResponse(
                    success=response.status == 200,
                    status_code=response.status,
                    payload=data,
                )

    async def post(
        self,
        endpoint: str,
        **kwargs,
    ):

        async with aiohttp.ClientSession(
            timeout=self.timeout,
        ) as session:

            async with session.post(
                self.base_url + endpoint,
                **kwargs,
            ) as response:

                data = await response.json()

                return RestResponse(
                    success=response.status == 200,
                    status_code=response.status,
                    payload=data,
                )