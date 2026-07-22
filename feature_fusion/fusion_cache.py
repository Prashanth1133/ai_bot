class FusionCache:

    def __init__(self):

        self._cache = {}

    def put(

        self,

        key,

        value,

    ):

        self._cache[key] = value

    def get(

        self,

        key,

    ):

        return self._cache.get(key)

    def clear(self):

        self._cache.clear()