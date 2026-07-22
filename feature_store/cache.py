from collections import deque


class FeatureCache:

    def __init__(

        self,

        max_size=500

    ):

        self.cache = deque(

            maxlen=max_size

        )

    def add(self, feature):

        self.cache.append(feature)

    def history(self):

        return list(self.cache)