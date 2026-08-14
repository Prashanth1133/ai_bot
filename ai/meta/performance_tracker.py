class PerformanceTracker:

    def evaluate(
        self,
        trades,
    ):

        if not trades:
            return None

        wins = sum(
            1
            for t in trades
            if getattr(t, "pnl", getattr(t, "profit", 0)) > 0
        )

        return wins / len(trades)