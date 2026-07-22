from __future__ import annotations

from asyncio import Queue


class OrderQueue:

    def __init__(self):

        self.queue = Queue()

    async def put(self, order):

        await self.queue.put(order)

    async def get(self):

        return await self.queue.get()

    def empty(self):

        return self.queue.empty()

    def size(self):

        return self.queue.qsize()

    async def clear(self):

        while not self.queue.empty():
            await self.queue.get()
            self.queue.task_done()