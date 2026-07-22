from __future__ import annotations

import numpy as np


class VWAP:
    """
    Volume Weighted Average Price
    """

    @staticmethod
    def calculate(
        high,
        low,
        close,
        volume,
    ):

        high = np.asarray(high, dtype=float)
        low = np.asarray(low, dtype=float)
        close = np.asarray(close, dtype=float)
        volume = np.asarray(volume, dtype=float)

        typical = (
            high + low + close
        ) / 3.0

        cumulative_price = np.cumsum(
            typical * volume
        )

        cumulative_volume = np.cumsum(
            volume
        )

        return np.divide(
            cumulative_price,
            cumulative_volume,
            out=np.zeros_like(cumulative_price),
            where=cumulative_volume != 0,
        )

    @staticmethod
    def latest(
        high,
        low,
        close,
        volume,
    ):
        return VWAP.calculate(
            high,
            low,
            close,
            volume,
        )[-1]