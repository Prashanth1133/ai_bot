import numpy as np


class FusionValidator:

    @staticmethod
    def validate(vector):

        if vector is None:

            return False

        if len(vector) == 0:

            return False

        if np.isnan(vector).any():

            return False

        if np.isinf(vector).any():

            return False

        return True