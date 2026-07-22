from __future__ import annotations


class StrategyRegistry:

    def __init__(self):

        self._strategies = {}

    def register(
        self,
        name: str,
        strategy,
    ):

        self._strategies[name] = strategy

    def unregister(
        self,
        name: str,
    ):

        self._strategies.pop(name, None)

    def get(
        self,
        name: str,
    ):

        return self._strategies.get(name)

    def names(self):

        return list(self._strategies.keys())

    def all(self):

        return self._strategies