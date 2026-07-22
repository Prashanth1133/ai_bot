from __future__ import annotations


class CheckpointRegistry:

    def __init__(self):

        self._checkpoints = {}

    def register(
        self,
        checkpoint,
    ):

        self._checkpoints[
            checkpoint.name
        ] = checkpoint

    def get(
        self,
        name: str,
    ):

        return self._checkpoints.get(name)

    def remove(
        self,
        name: str,
    ):

        self._checkpoints.pop(name, None)

    def all(self):

        return list(
            self._checkpoints.values()
        )

    def clear(self):

        self._checkpoints.clear()