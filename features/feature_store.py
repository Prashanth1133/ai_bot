from collections import defaultdict


class FeatureStore:

    def __init__(self):

        self.features = defaultdict(dict)

    def update(

        self,

        symbol,

        name,

        value

    ):

        self.features[symbol][name] = value

    def get(

        self,

        symbol

    ):

        return self.features[symbol]