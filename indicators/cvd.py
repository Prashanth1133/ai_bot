from __future__ import annotations

import numpy as np


class CVD:
    """
    Cumulative Volume Delta
    """

    @staticmethod
    def calculate(delta):

        delta = np.asarray(
            delta,
            dtype=float,
        )

        return np.cumsum(delta)

    @staticmethod
    def latest(delta):

        return CVD.calculate(delta)[-1]

    @staticmethod
    def slope(delta):

        cvd = CVD.calculate(delta)

        if len(cvd) < 2:

            return 0.0

        return cvd[-1] - cvd[-2]