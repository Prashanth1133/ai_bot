class RegimeCache:

    def __init__(self):

        self._cache = {}

    def put(

        self,

        symbol,

        snapshot,

    ):

        self._cache[symbol] = snapshot

    def get(

        self,

        symbol,

    ):

        return self._cache.get(symbol)

    def clear(self):

        self._cache.clear()