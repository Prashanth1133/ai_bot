from __future__ import annotations

import asyncio
from typing import Optional


class ListenKeyManager:
    """
    Maintains Binance user data stream listen key.
    """

    def __init__(self, rest_client):

        self.rest = rest_client

        self.listen_key: Optional[str] = None

        self.keepalive_interval = 30 * 60

        self._task = None

    async def create(self):

        response = await self.rest.post(
            "/fapi/v1/listenKey"
        )

        self.listen_key = response.payload["listenKey"]

        return self.listen_key

    async def keepalive(self):

        while True:

            await asyncio.sleep(
                self.keepalive_interval
            )

            if self.listen_key is None:
                continue

            await self.rest.put(
                "/fapi/v1/listenKey",
                params={
                    "listenKey": self.listen_key
                },
            )

    async def close(self):

        if self.listen_key:

            await self.rest.delete(
                "/fapi/v1/listenKey",
                params={
                    "listenKey": self.listen_key
                },
            )

            self.listen_key = None