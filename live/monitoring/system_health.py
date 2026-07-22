from __future__ import annotations

from datetime import datetime


class SystemHealth:

    def __init__(self):

        self.components = {}

    ##########################################################

    def update(

        self,

        component,

        status,

    ):

        self.components[component] = {

            "status": status,

            "updated": datetime.utcnow(),

        }

    ##########################################################

    def healthy(self):

        return all(

            c["status"]

            for c in self.components.values()

        )

    ##########################################################

    def report(self):

        return {

            "healthy": self.healthy(),

            "components": self.components,

        }