from __future__ import annotations


class SystemRegistry:

    def __init__(self):

        self._components = {}

    def register(
        self,
        name: str,
        component,
    ):

        self._components[name] = component

    def get(
        self,
        name: str,
    ):

        return self._components.get(name)

    def remove(
        self,
        name: str,
    ):

        self._components.pop(name, None)

    def components(self):

        return dict(self._components)

    def clear(self):

        self._components.clear()