from __future__ import annotations


class MessageRouter:

    def __init__(self):

        self.handlers = {}

    def register(
        self,
        stream: str,
        handler,
    ):

        self.handlers[stream] = handler

    async def dispatch(
        self,
        stream: str,
        payload,
    ):

        handler = self.handlers.get(stream)

        if handler is None:
            return

        return await handler(payload)