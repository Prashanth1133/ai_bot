from __future__ import annotations

import numpy as np


class PointOfControl:
    """
    Point of Control (POC)

    Price level with maximum traded volume.
    """

    @staticmethod
    def calculate(
        price_levels,
        volume_levels,
    ):

        price_levels = np.asarray(
            price_levels,
            dtype=float,
        )

        volume_levels = np.asarray(
            volume_levels,
            dtype=float,
        )

        if len(price_levels) == 0:

            return np.nan

        idx = np.argmax(volume_levels)

        return float(price_levels[idx])