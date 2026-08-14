class VotingEngine:

    """
    Direction-preserving voting layer.

    Currently there is one authoritative AI signal,
    so the voting engine returns that direction unchanged.
    """

    def vote(self, signal):

        action = getattr(
            signal,
            "action",
            None,
        )

        if action in {
            "BUY",
            "SELL",
            "HOLD",
        }:

            return action

        side = getattr(
            signal,
            "side",
            None,
        )

        if side in {
            "BUY",
            "SELL",
            "HOLD",
        }:

            return side

        signal_value = getattr(
            signal,
            "signal",
            None,
        )

        if signal_value in {
            "BUY",
            "SELL",
            "HOLD",
        }:

            return signal_value

        return "HOLD"