class ConfigCache:

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

        default=None,

    ):

        return self._cache.get(

            key,

            default,

        )

    def clear(self):

        self._cache.clear()