class RewardEngine:

    """
    Rewards:
        TP Hit     +1
        Partial TP +0.5
        HOLD       +0.1
        SL Hit     -1
        Liquidated -5
    """

    def compute(

        self,
        trade

    ):

        pnl = trade.pnl

        if pnl >= 0.03:
            return 1.0

        if pnl >= 0.01:
            return 0.5

        if pnl >= 0:

            return 0.1

        if pnl <= -0.05:

            return -5.0

        return -1.0