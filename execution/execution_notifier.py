from __future__ import annotations


class ExecutionNotifier:

    def __init__(self):

        self._listeners = []

    def subscribe(
        self,
        callback,
    ):

        self._listeners.append(callback)

    async def notify(
        self,
        event,
    ):

        for listener in self._listeners:

            await listener(event)