class RegimeRegistry:

    def __init__(self):

        self._registry = {}

    def update(

        self,

        symbol,

        snapshot,

    ):

        self._registry[symbol] = snapshot

    def get(

        self,

        symbol,

    ):

        return self._registry.get(symbol)

    def remove(

        self,

        symbol,

    ):

        self._registry.pop(symbol, None)

    def clear(self):

        self._registry.clear()

    def all(self):

        return list(self._registry.values())