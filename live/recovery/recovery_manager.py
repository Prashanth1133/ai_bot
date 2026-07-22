from __future__ import annotations

import asyncio


class RecoveryManager:

    def __init__(self):

        self.registry = None

    def attach(
        self,
        registry,
    ):

        self.registry = registry

    async def recover(
        self,
        component: str,
    ):

        handler = self.registry.get(component)

        if handler is None:

            return False

        result = handler()

        if asyncio.iscoroutine(result):

            result = await result

        return result