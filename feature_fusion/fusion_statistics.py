import numpy as np


class FusionStatistics:

    @staticmethod
    def summarize(vector):

        return {

            "size": len(vector),

            "mean": float(np.mean(vector)),

            "std": float(np.std(vector)),

            "min": float(np.min(vector)),

            "max": float(np.max(vector)),

        }