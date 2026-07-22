from __future__ import annotations


class DecisionRegistry:

    def __init__(self):

        self._engines = {}

    def register(
        self,
        name,
        engine,
    ):

        self._engines[name] = engine

    def get(
        self,
        name,
    ):

        return self._engines.get(name)

    def remove(
        self,
        name,
    ):

        self._engines.pop(name, None)

    def available(self):

        return list(self._engines.keys())