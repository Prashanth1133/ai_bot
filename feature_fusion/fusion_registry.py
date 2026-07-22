class FusionRegistry:

    def __init__(self):

        self._sources = {}

    def register(

        self,

        name,

        extractor,

    ):

        self._sources[name] = extractor

    def get(self, name):

        return self._sources.get(name)

    def all(self):

        return self._sources.items()

    def clear(self):

        self._sources.clear()