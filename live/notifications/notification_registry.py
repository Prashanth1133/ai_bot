from __future__ import annotations


class NotificationRegistry:

    def __init__(self):

        self._channels = {}

    def register(
        self,
        name: str,
        handler,
    ):

        self._channels[name] = handler

    def get(
        self,
        name: str,
    ):

        return self._channels.get(name)

    def remove(
        self,
        name: str,
    ):

        self._channels.pop(name, None)

    def channels(self):

        return dict(self._channels)

    def clear(self):

        self._channels.clear()