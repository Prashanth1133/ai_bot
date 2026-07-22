from __future__ import annotations

import numpy as np


class RSI:
    """
    Relative Strength Index (Wilder)
    """

    def __init__(self, period: int = 14):
        self.period = period

    def calculate(self, close):

        close = np.asarray(close, dtype=float)

        if len(close) < self.period + 1:
            return np.full(len(close), np.nan)

        delta = np.diff(close)

        gain = np.where(delta > 0, delta, 0.0)
        loss = np.where(delta < 0, -delta, 0.0)

        avg_gain = np.zeros(len(close))
        avg_loss = np.zeros(len(close))

        avg_gain[self.period] = np.mean(gain[: self.period])
        avg_loss[self.period] = np.mean(loss[: self.period])

        for i in range(self.period + 1, len(close)):
            avg_gain[i] = (
                avg_gain[i - 1] * (self.period - 1)
                + gain[i - 1]
            ) / self.period

            avg_loss[i] = (
                avg_loss[i - 1] * (self.period - 1)
                + loss[i - 1]
            ) / self.period

        rs = np.divide(
            avg_gain,
            avg_loss,
            out=np.zeros_like(avg_gain),
            where=avg_loss != 0,
        )

        rsi = 100.0 - (100.0 / (1.0 + rs))
        rsi[: self.period] = np.nan

        return rsi

    def latest(self, close):
        return self.calculate(close)[-1]