from __future__ import annotations

import numpy as np


class OBV:

    @staticmethod
    def calculate(
        close,
        volume,
    ):

        close = np.asarray(close)

        volume = np.asarray(volume)

        obv = np.zeros(len(close))

        for i in range(1, len(close)):

            if close[i] > close[i - 1]:

                obv[i] = (
                    obv[i - 1]
                    + volume[i]
                )

            elif close[i] < close[i - 1]:

                obv[i] = (
                    obv[i - 1]
                    - volume[i]
                )

            else:

                obv[i] = obv[i - 1]

        return obv

    @staticmethod
    def latest(
        close,
        volume,
    ):
        return OBV.calculate(
            close,
            volume,
        )[-1]