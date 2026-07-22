from __future__ import annotations

import numpy as np


class Momentum:

    def __init__(

        self,

        period=10,

    ):

        self.period = period

    def calculate(

        self,

        close,

    ):

        close = np.asarray(

            close,

            dtype=float,

        )

        momentum = np.full(

            len(close),

            np.nan,

        )

        momentum[self.period:] = (

            close[self.period:]

            - close[:-self.period]

        )

        return momentum

    def percentage(

        self,

        close,

    ):

        close = np.asarray(

            close,

            dtype=float,

        )

        pct = np.full(

            len(close),

            np.nan,

        )

        pct[self.period:] = (

            (close[self.period:] - close[:-self.period])

            / close[:-self.period]

        ) * 100

        return pct

    def latest(

        self,

        close,

    ):

        return self.calculate(close)[-1]