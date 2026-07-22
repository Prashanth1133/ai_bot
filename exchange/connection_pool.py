from __future__ import annotations

import aiohttp


class ConnectionPool:

    def __init__(self):

        self.connector = aiohttp.TCPConnector(
            limit=100,
            ttl_dns_cache=300,
        )

        self.session = aiohttp.ClientSession(
            connector=self.connector,
        )

    async def close(self):

        await self.session.close()