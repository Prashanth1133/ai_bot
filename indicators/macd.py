from __future__ import annotations

import numpy as np

from indicators.ema import EMA


class MACD:

    def __init__(
        self,
        fast: int = 12,
        slow: int = 26,
        signal: int = 9,
    ):
        self.fast = EMA(fast)
        self.slow = EMA(slow)
        self.signal = EMA(signal)

    def calculate(self, close):

        close = np.asarray(close, dtype=float)

        fast = self.fast.calculate(close)
        slow = self.slow.calculate(close)

        macd = fast - slow

        signal = self.signal.calculate(macd)

        histogram = macd - signal

        return {
            "macd": macd,
            "signal": signal,
            "histogram": histogram,
        }

    def latest(self, close):

        result = self.calculate(close)

        return {
            k: v[-1]
            for k, v in result.items()
        }