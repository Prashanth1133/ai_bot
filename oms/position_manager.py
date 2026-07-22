from decimal import Decimal


class PositionManager:

    def __init__(self):

        self.positions = {}

    def update(self, fill):

        symbol = fill.symbol

        if symbol not in self.positions:

            self.positions[symbol] = Decimal("0")

        if fill.side.upper() == "BUY":

            self.positions[symbol] += fill.quantity

        else:

            self.positions[symbol] -= fill.quantity

    def position(self, symbol):

        return self.positions.get(symbol, Decimal("0"))