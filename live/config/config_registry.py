from __future__ import annotations


class ConfigRegistry:

    def __init__(self):

        self._configs = {}

    def register(
        self,
        name: str,
        config,
    ):

        self._configs[name] = config

    def get(
        self,
        name: str,
    ):

        return self._configs.get(name)

    def update(
        self,
        name: str,
        config,
    ):

        self._configs[name] = config

    def remove(
        self,
        name: str,
    ):

        self._configs.pop(name, None)

    def clear(self):

        self._configs.clear()