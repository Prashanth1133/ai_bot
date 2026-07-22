from __future__ import annotations


class Service:

    async def start(self):

        raise NotImplementedError

    async def stop(self):

        raise NotImplementedError

    async def health(self):

        raise NotImplementedError