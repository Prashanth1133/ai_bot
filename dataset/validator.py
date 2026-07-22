from __future__ import annotations

import numpy as np


class DatasetValidator:

    @staticmethod
    def validate(

        features,

        labels,

    ):

        features = np.asarray(features)

        labels = np.asarray(labels)

        if len(features) == 0:

            return False

        if len(labels) == 0:

            return False

        if len(features) != len(labels):

            return False

        if np.isnan(features).any():

            return False

        if np.isnan(labels).any():

            return False

        return True