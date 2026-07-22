from __future__ import annotations


class WatchdogRegistry:

    def __init__(self):

        self._components = {}

    def register(
        self,
        component: str,
        callback,
    ):

        self._components[component] = callback

    def unregister(
        self,
        component: str,
    ):

        self._components.pop(component, None)

    def get(
        self,
        component: str,
    ):

        return self._components.get(component)

    def components(self):

        return dict(self._components)

    def clear(self):

        self._components.clear()