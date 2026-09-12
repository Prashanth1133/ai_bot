from __future__ import annotations

import numpy as np


class RSI:
    """
    Relative Strength Index (Wilder)
    """

    def __init__(self, period: int = 14):
        self.period = int(period)

    def calculate(self, close):
        close = np.asarray(
            close,
            dtype=np.float64,
        )

        n = len(close)

        if n == 0:
            return np.array(
                [],
                dtype=np.float64,
            )

        if n < self.period + 1:
            return np.full(
                n,
                50.0,
                dtype=np.float64,
            )

        delta = np.diff(close)

        gains = np.maximum(
            delta,
            0.0,
        )

        losses = np.maximum(
            -delta,
            0.0,
        )

        avg_gain = np.zeros(
            n,
            dtype=np.float64,
        )

        avg_loss = np.zeros(
            n,
            dtype=np.float64,
        )

        rsi = np.full(
            n,
            50.0,
            dtype=np.float64,
        )

        p = self.period

        avg_gain[p] = np.mean(
            gains[:p]
        )

        avg_loss[p] = np.mean(
            losses[:p]
        )

        for i in range(
            p + 1,
            n,
        ):
            avg_gain[i] = (
                (
                    avg_gain[i - 1]
                    * (p - 1)
                )
                + gains[i - 1]
            ) / p

            avg_loss[i] = (
                (
                    avg_loss[i - 1]
                    * (p - 1)
                )
                + losses[i - 1]
            ) / p

        valid = avg_loss > 0

        rs = np.zeros_like(
            avg_loss
        )

        rs[valid] = (
            avg_gain[valid]
            / avg_loss[valid]
        )

        rsi[valid] = (
            100.0
            - (
                100.0
                / (1.0 + rs[valid])
            )
        )

        rsi[
            (avg_loss == 0)
            & (avg_gain > 0)
        ] = 100.0

        return rsi

    def latest(self, close):
        calc = self.calculate(close)
        return float(calc[-1]) if len(calc) > 0 else 50.0