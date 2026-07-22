from __future__ import annotations


class QueueManager:

    def __init__(self):

        self.registry = None

    def attach(
        self,
        registry,
    ):

        self.registry = registry

    def queue(
        self,
        name,
    ):

        return self.registry.get(name)

    async def publish(
        self,
        name,
        item,
    ):

        queue = self.registry.get(name)

        if queue is None:
            return

        await queue.put(item)