from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal


@dataclass(slots=True)
class SwingPoint:

    price: Decimal
    candle: object
    is_high: bool


class AdaptiveSwingDetector:

    def __init__(
        self,
        multiplier: float = 1.5,
    ):
        self.multiplier = float(
            multiplier
        )

    def detect(
        self,
        candles,
        atr,
    ):

        if atr is None or not candles:
            return []

        threshold = (
            Decimal(str(float(atr)))
            * Decimal(str(self.multiplier))
        )

        if threshold <= 0:
            return []

        swings = []

        last_high = candles[0].high
        last_low = candles[0].low

        for candle in candles[1:]:

            high_move = (
                candle.high - last_high
            )

            low_move = (
                last_low - candle.low
            )

            if high_move > threshold:

                last_high = candle.high

                swings.append(
                    SwingPoint(
                        price=candle.high,
                        candle=candle,
                        is_high=True,
                    )
                )

            if low_move > threshold:

                last_low = candle.low

                swings.append(
                    SwingPoint(
                        price=candle.low,
                        candle=candle,
                        is_high=False,
                    )
                )

        return swings

    def reset(self):
        pass