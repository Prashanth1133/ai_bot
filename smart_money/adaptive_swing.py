from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal


@dataclass(slots=True)
class SwingPoint:

    price: Decimal

    candle: object

    is_high: bool


class AdaptiveSwingDetector:

    """
    ATR-based adaptive swing detector.
    """

    def __init__(self):

        self.last_high = {}

        self.last_low = {}

    def detect(

        self,

        candles,

        atr

    ):

        if atr is None:

            return []

        symbol = candles[-1].symbol

        if symbol not in self.last_high:

            self.last_high[symbol] = candles[0].high

            self.last_low[symbol] = candles[0].low

        swings = []

        threshold = atr * Decimal("1.5")

        for candle in candles:

            if candle.high - self.last_high[symbol] > threshold:

                self.last_high[symbol] = candle.high

                swings.append(

                    SwingPoint(

                        candle=candle,

                        price=candle.high,

                        is_high=True

                    )

                )

            if self.last_low[symbol] - candle.low > threshold:

                self.last_low[symbol] = candle.low

                swings.append(

                    SwingPoint(

                        candle=candle,

                        price=candle.low,

                        is_high=False

                    )

                )

        return swings