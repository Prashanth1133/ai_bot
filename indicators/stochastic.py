from __future__ import annotations

import numpy as np


class Stochastic:

    def __init__(
        self,
        period=14,
        smooth=3,
    ):

        self.period = period

        self.smooth = smooth

    def calculate(
        self,
        high,
        low,
        close,
    ):

        high = np.asarray(high)

        low = np.asarray(low)

        close = np.asarray(close)

        k = np.full(len(close), np.nan)

        for i in range(
            self.period - 1,
            len(close),
        ):

            highest = np.max(
                high[
                    i - self.period + 1 : i + 1
                ]
            )

            lowest = np.min(
                low[
                    i - self.period + 1 : i + 1
                ]
            )

            if highest != lowest:

                k[i] = (
                    (close[i] - lowest)
                    / (highest - lowest)
                ) * 100

        d = np.copy(k)

        for i in range(
            self.period,
            len(close),
        ):

            d[i] = np.nanmean(
                k[
                    i - self.smooth + 1 : i + 1
                ]
            )

        return {

            "k": k,

            "d": d,

        }

    def latest(
        self,
        high,
        low,
        close,
    ):

        result = self.calculate(
            high,
            low,
            close,
        )

        return {
            k: v[-1]
            for k, v in result.items()
        }