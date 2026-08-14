# ==========================================
# paper_trading/performance.py
# ==========================================


class PerformanceManager:

    def __init__(self):

        self.trades = []

    def record_trade(self, trade):

        if trade is not None:
            self.trades.append(trade)

    def calculate(
        self,
        trades=None
    ):

        target_trades = trades if trades is not None else self.trades

        total = len(target_trades)

        wins = 0

        losses = 0

        profit = 0

        for trade in target_trades:

            pnl = trade["pnl"] if isinstance(trade, dict) else getattr(trade, "pnl", 0)

            profit += pnl

            if pnl > 0:

                wins += 1

            elif pnl < 0:

                losses += 1

        winrate = 0

        if total > 0:

            winrate = (wins / total) * 100

        return {
            "total_trades": total,
            "wins": wins,
            "losses": losses,
            "winrate": round(winrate, 2),
            "profit": round(profit, 2)
        }


# Alias for backward compatibility
PerformanceTracker = PerformanceManager