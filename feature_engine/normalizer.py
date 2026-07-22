import numpy as np


class FeatureNormalizer:

    """
    Min-Max normalization.
    """

    def normalize(self, vector):

        minimum = np.min(vector)

        maximum = np.max(vector)

        if maximum == minimum:

            return vector

        return (

            vector - minimum

        ) / (

            maximum - minimum

        )