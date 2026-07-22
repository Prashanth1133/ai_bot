from __future__ import annotations

import inspect


class OrderDispatcher:

    def __init__(
        self,
        router,
    ):

        self.router = router

    async def dispatch(
        self,
        mode,
        order,
    ):

        result = self.router.execute(
            mode,
            order,
        )

        if inspect.isawaitable(result):
            result = await result

        return result