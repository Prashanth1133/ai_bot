class PortfolioManager:
    """Minimal directional paper portfolio with executable TP/SL levels."""

    def __init__(self, capital=10000):
        self.initial_capital = capital
        self.balance = capital
        self.positions = {}
        self.closed_trades = []

    def open_position(self, signal):
        self.positions[signal.symbol] = {
            "entry": signal.entry_price,
            "quantity": getattr(signal, "quantity", 1),
            "side": signal.action,
            "take_profit": signal.take_profit,
            "stop_loss": signal.stop_loss,
        }

    def close_position(self, signal):
        if signal.symbol not in self.positions:
            return None

        position = self.positions[signal.symbol]
        price = signal.entry_price
        direction = 1 if position["side"] == "BUY" else -1
        pnl = (price - position["entry"]) * position["quantity"] * direction
        self.balance += pnl
        trade = {
            "symbol": signal.symbol,
            "entry": position["entry"],
            "exit": price,
            "quantity": position["quantity"],
            "side": position["side"],
            "pnl": pnl,
        }
        self.closed_trades.append(trade)
        del self.positions[signal.symbol]
        return trade

    def get_balance(self):
        return self.balance

    def get_positions(self):
        return self.positions

    def get_trades(self):
        return self.closed_trades


Portfolio = PortfolioManager
