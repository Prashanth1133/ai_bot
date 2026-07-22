from __future__ import annotations

import numpy as np

from indicators.atr import ATR


class SuperTrend:

    def __init__(
        self,
        period=10,
        multiplier=3.0,
    ):

        self.atr = ATR(period)

        self.multiplier = multiplier

    def calculate(
        self,
        high,
        low,
        close,
    ):

        atr = self.atr.calculate(
            high,
            low,
            close,
        )

        hl2 = (
            np.asarray(high)
            + np.asarray(low)
        ) / 2.0

        upper = hl2 + self.multiplier * atr

        lower = hl2 - self.multiplier * atr

        trend = np.ones(len(close))

        for i in range(1, len(close)):

            if close[i] > upper[i - 1]:
                trend[i] = 1

            elif close[i] < lower[i - 1]:
                trend[i] = -1

            else:
                trend[i] = trend[i - 1]

        return trend

    def latest(
        self,
        high,
        low,
        close,
    ):
        return self.calculate(
            high,
            low,
            close,
        )[-1]