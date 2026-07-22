from collections import defaultdict


class LifecycleMetrics:

    def __init__(self):

        self.transitions = defaultdict(int)

    def record(

        self,

        state,

    ):

        self.transitions[
            state
        ] += 1

    def statistics(self):

        return dict(
            self.transitions
        )