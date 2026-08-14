from app.config import DEFAULT_SYMBOL


class CoinManager:

    def __init__(self):

        self._symbol = DEFAULT_SYMBOL

    def current(self):

        return self._symbol

    def set(self, symbol):

        self._symbol = symbol.lower()
