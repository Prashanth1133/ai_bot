class LifecycleRegistry:

    def __init__(self):

        self._states = {}

    def update(

        self,

        component: str,

        state,

    ):

        self._states[component] = state

    def get(

        self,

        component: str,

    ):

        return self._states.get(component)

    def all(self):

        return dict(self._states)

    def clear(self):

        self._states.clear()