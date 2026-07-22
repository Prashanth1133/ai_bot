from __future__ import annotations

import numpy as np


class VolumeProfileStatistics:

    @staticmethod
    def summarize(

        histogram,

    ):

        volume = histogram["volume"]

        return {

            "max_volume": float(

                np.max(volume)

            ),

            "min_volume": float(

                np.min(volume)

            ),

            "mean_volume": float(

                np.mean(volume)

            ),

            "std_volume": float(

                np.std(volume)

            ),

            "total_volume": float(

                np.sum(volume)

            ),

        }