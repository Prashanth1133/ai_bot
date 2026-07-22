from __future__ import annotations

import asyncio
from typing import Awaitable, Callable, TypeVar

T = TypeVar("T")


class RetryManager:
    """
    Generic async retry utility.
    """

    def __init__(
        self,
        retries: int = 3,
        delay: float = 0.5,
        backoff: float = 2.0,
    ):
        self.retries = retries
        self.delay = delay
        self.backoff = backoff

    async def run(
        self,
        fn: Callable[..., Awaitable[T]],
        *args,
        **kwargs,
    ) -> T:

        current_delay = self.delay
        last_exception = None

        for _ in range(self.retries):
            try:
                return await fn(*args, **kwargs)

            except Exception as exc:
                last_exception = exc
                await asyncio.sleep(current_delay)
                current_delay *= self.backoff

        raise last_exception