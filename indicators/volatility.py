from __future__ import annotations

import numpy as np


class Volatility:

    @staticmethod
    def returns(close):

        close = np.asarray(
            close,
            dtype=float,
        )

        return np.diff(
            np.log(close)
        )

    @staticmethod
    def calculate(

        close,

        window=20,

    ):

        r = Volatility.returns(
            close
        )

        if len(r) < window:

            return np.nan

        return np.std(
            r[-window:]
        ) * np.sqrt(365)

    @staticmethod
    def series(

        close,

        window=20,

    ):

        close = np.asarray(
            close,
            dtype=float,
        )

        values = np.full(
            len(close),
            np.nan,
        )

        for i in range(

            window,

            len(close),

        ):

            values[i] = Volatility.calculate(

                close[: i + 1],

                window,

            )

        return values