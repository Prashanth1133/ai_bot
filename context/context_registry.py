class ContextRegistry:

    def __init__(self):

        self._providers = {}

    def register(

        self,

        name,

        provider,

    ):

        self._providers[name] = provider

    def provider(

        self,

        name,

    ):

        return self._providers.get(name)

    def providers(self):

        return self._providers.items()

    def clear(self):

        self._providers.clear()