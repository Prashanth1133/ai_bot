from __future__ import annotations

import numpy as np

from indicators.ema import EMA


class Trend:

    def __init__(

        self,

        fast=20,

        slow=50,

    ):

        self.fast = EMA(fast)

        self.slow = EMA(slow)

    def calculate(

        self,

        close,

    ):

        fast = self.fast.calculate(close)

        slow = self.slow.calculate(close)

        trend = np.zeros(

            len(close),

            dtype=int,

        )

        trend[fast > slow] = 1

        trend[fast < slow] = -1

        return trend

    def latest(

        self,

        close,

    ):

        return self.calculate(close)[-1]