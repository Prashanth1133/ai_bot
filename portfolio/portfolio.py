class Portfolio:

    def __init__(self):

        self.cash = 10000.0

        self.positions = {}

    def add(self, position):

        self.positions[position.symbol] = position

    def remove(self, symbol):

        self.positions.pop(symbol, None)

    def total_value(self):

        total = self.cash

        for p in self.positions.values():

            total += p.current_price * p.quantity

        return total