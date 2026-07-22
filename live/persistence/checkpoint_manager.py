from __future__ import annotations

from live.persistence.checkpoint import Checkpoint


class CheckpointManager:

    def __init__(self):

        self.registry = None

    def attach(
        self,
        registry,
    ):

        self.registry = registry

    def create(
        self,
        name: str,
        state: dict,
    ):

        checkpoint = Checkpoint(
            name=name,
            state=state,
        )

        self.registry.register(
            checkpoint
        )

        return checkpoint

    def load(
        self,
        name: str,
    ):

        checkpoint = self.registry.get(
            name
        )

        if checkpoint is None:

            return None

        return checkpoint.state