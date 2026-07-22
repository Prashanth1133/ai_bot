from collections import deque


class DecisionMetrics:

    def __init__(self):

        self.decisions = 0
        self.approved = 0
        self.rejected = 0

        self.history = deque(maxlen=10000)

    def update(
        self,
        decision,
    ):

        self.decisions += 1

        if decision.approved:
            self.approved += 1
        else:
            self.rejected += 1

        self.history.append(decision)

    @property
    def approval_rate(self):

        if self.decisions == 0:
            return 0.0

        return (
            self.approved
            / self.decisions
        )