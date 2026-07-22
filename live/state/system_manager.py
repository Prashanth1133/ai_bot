from __future__ import annotations

from live.state.system_context import SystemContext
from live.state.system_state import SystemState


class SystemManager:

    def __init__(self):

        self.context = SystemContext()

    def state(self):

        return SystemState(
            self.context.state
        )

    def transition(
        self,
        state: SystemState,
    ):

        self.context.state = state.value

    def metadata(self):

        return self.context.metadata