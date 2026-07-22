from __future__ import annotations

import inspect


class ExecutionRouter:

    def __init__(self):

        self._routes = {}

    def register(
        self,
        name: str,
        executor,
    ):

        self._routes[name] = executor

    def unregister(
        self,
        name: str,
    ):

        self._routes.pop(name, None)

    async def execute(
        self,
        name: str,
        order,
    ):

        executor = self._routes.get(name)

        if executor is None:
            raise ValueError(
                f"Unknown execution route: {name}"
            )

        result = executor.execute(order)

        if inspect.isawaitable(result):
            result = await result

        return result

    def routes(self):

        return list(self._routes.keys())