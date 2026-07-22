from __future__ import annotations

import numpy as np


class EMA:
    """
    Exponential Moving Average
    """

    def __init__(self, period: int = 20):
        self.period = period

    def calculate(self, close: np.ndarray) -> np.ndarray:
        close = np.asarray(close, dtype=float)

        if len(close) == 0:
            return np.array([])

        alpha = 2.0 / (self.period + 1.0)

        ema = np.zeros_like(close, dtype=float)
        ema[0] = close[0]

        for i in range(1, len(close)):
            ema[i] = alpha * close[i] + (1.0 - alpha) * ema[i - 1]

        return ema

    def latest(self, close):
        return self.calculate(close)[-1]