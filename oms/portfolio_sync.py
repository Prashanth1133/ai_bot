from __future__ import annotations


class PortfolioSync:

    def __init__(self):

        self._listeners = []

    def subscribe(
        self,
        callback,
    ):

        self._listeners.append(callback)

    async def publish(
        self,
        portfolio,
    ):

        for callback in self._listeners:

            await callback(portfolio)