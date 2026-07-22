from models.state import SymbolState


class MarketCache:

    def __init__(self):

        self.symbols = {}

    def get(self, symbol: str) -> SymbolState:

        if symbol not in self.symbols:

            self.symbols[symbol] = SymbolState(symbol)

        return self.symbols[symbol]