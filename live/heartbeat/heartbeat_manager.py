from __future__ import annotations

from live.heartbeat.heartbeat import Heartbeat


class HeartbeatManager:

    def __init__(self):

        self.registry = None

    def attach(
        self,
        registry,
    ):

        self.registry = registry

    def beat(

        self,

        component: str,

        healthy: bool = True,

        message: str = "",

    ):

        heartbeat = Heartbeat(

            component=component,

            healthy=healthy,

            message=message,

        )

        self.registry.update(
            heartbeat
        )

        return heartbeat