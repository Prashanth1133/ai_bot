class ReinforcementEngine:

    def __init__(self):

        self.reward = 0

    def update(
        self,
        pnl
    ):

        self.reward += pnl

        return self.reward