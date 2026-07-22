class PerformanceTracker:

    def evaluate(

        self,

        trades,

    ):

        if not trades:

            return 0.0

        wins = sum(

            1

            for t in trades

            if t.pnl > 0

        )

        return wins / len(trades)