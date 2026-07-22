from __future__ import annotations

import numpy as np


class ValueArea:
    """
    70% Value Area
    """

    @staticmethod
    def calculate(

        price_levels,

        volume_levels,

        percentage=0.70,

    ):

        price_levels = np.asarray(
            price_levels,
            dtype=float,
        )

        volume_levels = np.asarray(
            volume_levels,
            dtype=float,
        )

        order = np.argsort(
            volume_levels
        )[::-1]

        total = volume_levels.sum()

        cumulative = 0.0

        selected = []

        for idx in order:

            cumulative += volume_levels[idx]

            selected.append(idx)

            if cumulative >= total * percentage:

                break

        prices = price_levels[selected]

        return {

            "vah": float(prices.max()),

            "val": float(prices.min()),

        }