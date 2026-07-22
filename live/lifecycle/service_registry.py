from __future__ import annotations


class ServiceRegistry:

    def __init__(self):

        self._services = {}

    def register(
        self,
        name,
        service,
    ):

        self._services[name] = service

    def get(
        self,
        name,
    ):

        return self._services.get(name)

    def services(self):

        return list(
            self._services.values()
        )

    def clear(self):

        self._services.clear()