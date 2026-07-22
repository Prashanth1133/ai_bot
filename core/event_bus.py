import asyncio
from collections import defaultdict
from typing import Callable, Awaitable, Any

from app.logger import logger

Handler = Callable[[Any], Awaitable[None]]


class EventBus:

    def __init__(self):
        self._subscribers = defaultdict(list)

    def subscribe(self, topic: str, handler: Handler):
        self._subscribers[topic].append(handler)

    async def publish(self, topic: str, message: Any):

        if topic not in self._subscribers:
            return

        tasks = [
            asyncio.create_task(handler(message))
            for handler in self._subscribers[topic]
        ]

        results = await asyncio.gather(
            *tasks,
            return_exceptions=True
        )

        for result in results:
            if isinstance(result, Exception):
                logger.exception(result)