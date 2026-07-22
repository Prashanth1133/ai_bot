from __future__ import annotations


class ResourceRegistry:

    def __init__(self):

        self._resources = {}

    def update(
        self,
        resource,
    ):

        self._resources[
            resource.name
        ] = resource

    def get(
        self,
        name: str,
    ):

        return self._resources.get(name)

    def all(self):

        return list(
            self._resources.values()
        )

    def clear(self):

        self._resources.clear()