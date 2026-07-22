from __future__ import annotations


class RecoveryRegistry:

    def __init__(self):

        self._handlers = {}

    def register(
        self,
        name: str,
        handler,
    ):

        self._handlers[name] = handler

    def get(
        self,
        name: str,
    ):

        return self._handlers.get(name)

    def remove(
        self,
        name: str,
    ):

        self._handlers.pop(name, None)

    def handlers(self):

        return dict(self._handlers)

    def clear(self):

        self._handlers.clear()