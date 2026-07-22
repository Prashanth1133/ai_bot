from __future__ import annotations


class ResourceManager:

    def __init__(self):

        self.registry = None

    def attach(
        self,
        registry,
    ):

        self.registry = registry

    def resources(self):

        return self.registry.all()

    def resource(
        self,
        name: str,
    ):

        return self.registry.get(name)