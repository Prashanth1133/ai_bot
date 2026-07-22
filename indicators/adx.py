from __future__ import annotations

import numpy as np


class ADX:
    """
    Average Directional Index
    """

    def __init__(self, period: int = 14):
        self.period = period

    def calculate(
        self,
        high,
        low,
        close,
    ):

        high = np.asarray(high, dtype=float)
        low = np.asarray(low, dtype=float)
        close = np.asarray(close, dtype=float)

        length = len(close)

        if length < self.period + 1:
            return np.full(length, np.nan)

        plus_dm = np.zeros(length)
        minus_dm = np.zeros(length)
        tr = np.zeros(length)

        for i in range(1, length):

            up = high[i] - high[i - 1]
            down = low[i - 1] - low[i]

            plus_dm[i] = up if up > down and up > 0 else 0
            minus_dm[i] = down if down > up and down > 0 else 0

            tr[i] = max(
                high[i] - low[i],
                abs(high[i] - close[i - 1]),
                abs(low[i] - close[i - 1]),
            )

        atr = np.zeros(length)

        atr[self.period] = np.mean(
            tr[1 : self.period + 1]
        )

        for i in range(self.period + 1, length):

            atr[i] = (
                atr[i - 1] * (self.period - 1)
                + tr[i]
            ) / self.period

        plus_di = np.divide(
            100 * plus_dm,
            atr,
            out=np.zeros(length),
            where=atr != 0,
        )

        minus_di = np.divide(
            100 * minus_dm,
            atr,
            out=np.zeros(length),
            where=atr != 0,
        )

        dx = np.divide(
            np.abs(plus_di - minus_di),
            plus_di + minus_di,
            out=np.zeros(length),
            where=(plus_di + minus_di) != 0,
        ) * 100

        adx = np.zeros(length)

        adx[self.period] = np.mean(
            dx[1 : self.period + 1]
        )

        for i in range(self.period + 1, length):

            adx[i] = (
                adx[i - 1] * (self.period - 1)
                + dx[i]
            ) / self.period

        adx[: self.period] = np.nan

        return adx

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