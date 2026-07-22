import numpy as np


class FeatureNormalizer:

    """
    Online z-score normalization.
    """

    def normalize(

        self,

        vector

    ):

        result = {}

        for k, v in vector.items():

            if isinstance(v, (int, float)):

                result[k] = float(v)

            else:

                result[k] = v

        return result