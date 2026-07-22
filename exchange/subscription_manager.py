from __future__ import annotations


class SubscriptionManager:

    def __init__(self):

        self._subscriptions = set()

    def subscribe(
        self,
        stream: str,
    ):

        self._subscriptions.add(
            stream.lower()
        )

    def unsubscribe(
        self,
        stream: str,
    ):

        self._subscriptions.discard(
            stream.lower()
        )

    def subscribed(
        self,
        stream: str,
    ):

        return stream.lower() in self._subscriptions

    def all(self):

        return sorted(self._subscriptions)

    def clear(self):

        self._subscriptions.clear()