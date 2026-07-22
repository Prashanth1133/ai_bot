from __future__ import annotations

import numpy as np


class Delta:
    """
    Trade Delta

    Delta = Buy Volume - Sell Volume
    """

    @staticmethod
    def calculate(
        buy_volume,
        sell_volume,
    ):

        buy = np.asarray(
            buy_volume,
            dtype=float,
        )

        sell = np.asarray(
            sell_volume,
            dtype=float,
        )

        return buy - sell

    @staticmethod
    def cumulative(delta):

        return np.cumsum(delta)

    @staticmethod
    def latest(
        buy_volume,
        sell_volume,
    ):

        return Delta.calculate(
            buy_volume,
            sell_volume,
        )[-1]