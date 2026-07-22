from __future__ import annotations


class HeartbeatRegistry:

    def __init__(self):

        self._heartbeats = {}

    def update(
        self,
        heartbeat,
    ):

        self._heartbeats[
            heartbeat.component
        ] = heartbeat

    def get(
        self,
        component: str,
    ):

        return self._heartbeats.get(component)

    def all(self):

        return list(
            self._heartbeats.values()
        )

    def clear(self):

        self._heartbeats.clear()