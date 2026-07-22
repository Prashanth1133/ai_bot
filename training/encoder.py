import numpy as np


class FeatureEncoder:

    """
    Converts dictionary features
    into ordered numeric vectors.
    """

    def __init__(self, feature_order):

        self.feature_order = feature_order

    def encode(self, features):

        row = []

        for key in self.feature_order:

            value = features.get(key, 0.0)

            if isinstance(value, bool):
                value = float(value)

            elif isinstance(value, str):
                value = 0.0

            row.append(float(value))

        return np.asarray(

            row,

            dtype=np.float32

        )