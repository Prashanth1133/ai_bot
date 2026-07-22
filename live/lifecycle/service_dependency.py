from __future__ import annotations


class ServiceDependency:

    def __init__(self):

        self.dependencies = {}

    def add(
        self,
        service,
        depends_on,
    ):

        self.dependencies.setdefault(
            service,
            set(),
        ).add(depends_on)

    def get(
        self,
        service,
    ):

        return list(
            self.dependencies.get(
                service,
                set(),
            )
        )

    def clear(self):

        self.dependencies.clear()