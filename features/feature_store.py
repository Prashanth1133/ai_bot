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
        symbol,
        feature=None
    ):
        if feature is not None:
            return self.features[symbol].get(feature)
        return self.features[symbol]

    def get_all(
        self,
        symbol
    ):

        return self.features[symbol]

    def clear(
        self,
        symbol
    ):

        if symbol in self.features:
            self.features[symbol].clear()