from live.lifecycle.lifecycle_event import (
    LifecycleEvent,
)


class LifecycleManager:

    def __init__(

        self,

        registry,

        history=None,

    ):

        self.registry = registry

        self.history = history

    def transition(

        self,

        component,

        new_state,

        metadata=None,

    ):

        previous = self.registry.get(
            component
        )

        self.registry.update(
            component,
            new_state,
        )

        event = LifecycleEvent(

            component=component,

            previous_state=(
                previous.name
                if previous
                else ""
            ),

            current_state=new_state.name,

            metadata=metadata or {},

        )

        if self.history:

            self.history.add(event)

        return event