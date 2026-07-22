from __future__ import annotations

import asyncio


class PriorityQueue:

    def __init__(self):

        self._queue = asyncio.PriorityQueue()

    async def put(
        self,
        item,
    ):

        await self._queue.put(
            (
                item.priority,
                item,
            )
        )

    async def get(self):

        _, item = await self._queue.get()

        return item

    def empty(self):

        return self._queue.empty()

    def size(self):

        return self._queue.qsize()