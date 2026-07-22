from __future__ import annotations

import numpy as np


class BollingerBands:

    def __init__(
        self,
        period=20,
        std=2.0,
    ):
        self.period = period
        self.std = std

    def calculate(self, close):

        close = np.asarray(close, dtype=float)

        upper = np.full(len(close), np.nan)
        middle = np.full(len(close), np.nan)
        lower = np.full(len(close), np.nan)

        for i in range(
            self.period - 1,
            len(close),
        ):

            window = close[
                i - self.period + 1 : i + 1
            ]

            mean = np.mean(window)

            sigma = np.std(window)

            middle[i] = mean
            upper[i] = mean + sigma * self.std
            lower[i] = mean - sigma * self.std

        return {
            "upper": upper,
            "middle": middle,
            "lower": lower,
        }

    def latest(self, close):

        data = self.calculate(close)

        return {
            k: v[-1]
            for k, v in data.items()
        }