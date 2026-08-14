# ==========================================
# paper_trading/tracker.py
# ==========================================


class TradeTracker:

    def __init__(self):

        self.total_profit = 0

        self.total_loss = 0

        self.active_positions = {}

    def open(self, signal):

        if hasattr(signal, "symbol"):
            self.active_positions[signal.symbol] = signal

    def close(self, trade):

        if isinstance(trade, dict):
            pnl = trade.get("pnl", 0)
            symbol = trade.get("symbol")
        else:
            pnl = getattr(trade, "pnl", 0)
            symbol = getattr(trade, "symbol", None)

        if symbol:
            self.active_positions.pop(symbol, None)

        self.update(pnl)

    def update(
        self,
        pnl
    ):

        if pnl > 0:

            self.total_profit += pnl

        elif pnl < 0:

            self.total_loss += abs(pnl)

    def report(self):

        return {
            "profit": round(self.total_profit, 2),
            "loss": round(self.total_loss, 2)
        }