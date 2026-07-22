from __future__ import annotations

import numpy as np


class DatasetStatistics:

    @staticmethod
    def summarize(features):

        features = np.asarray(features)

        return {

            "rows": int(features.shape[0]),

            "columns": int(features.shape[1]),

            "mean": np.mean(features, axis=0),

            "std": np.std(features, axis=0),

            "min": np.min(features, axis=0),

            "max": np.max(features, axis=0),

        }