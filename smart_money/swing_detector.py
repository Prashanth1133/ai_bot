from dataclasses import dataclass

from models.market import Candle


@dataclass(slots=True)
class SwingPoint:

    candle: Candle

    price: float

    index: int

    is_high: bool

    class SwingDetector:

    """
    Detects swing highs and lows using
    a configurable lookback window.
    """

    def __init__(self, window: int = 2):

        self.window = window

    def detect(self, candles):

        swings = []

        if len(candles) < (self.window * 2 + 1):

            return swings

        for i in range(self.window, len(candles) - self.window):

            current = candles[i]

            left = candles[i - self.window:i]

            right = candles[i + 1:i + self.window + 1]

            if all(current.high > c.high for c in left) and \
               all(current.high > c.high for c in right):

                swings.append(
                    SwingPoint(
                        candle=current,
                        price=float(current.high),
                        index=i,
                        is_high=True
                    )
                )

            if all(current.low < c.low for c in left) and \
               all(current.low < c.low for c in right):

                swings.append(
                    SwingPoint(
                        candle=current,
                        price=float(current.low),
                        index=i,
                        is_high=False
                    )
                )

        return swings