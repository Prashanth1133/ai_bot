class ExchangeRegistry:

    def __init__(self):

        self._registry = {}

    def register(
        self,
        name,
        exchange,
    ):

        self._registry[name] = exchange

    def get(
        self,
        name,
    ):

        return self._registry.get(name)

    def remove(
        self,
        name,
    ):

        self._registry.pop(name, None)

    def exchanges(self):

        return list(self._registry.keys())