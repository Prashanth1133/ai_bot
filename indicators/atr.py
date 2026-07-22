from __future__ import annotations

from collections import defaultdict, deque
from decimal import Decimal


class ATRCalculator:
    """
    Symbol-aware ATR calculator.
    Maintains an independent ATR state for each symbol/timeframe.
    """

    def __init__(self, period: int = 14):

        self.period = period

        self.tr = defaultdict(lambda: deque(maxlen=period))

        self.previous_close = {}

    def update(self, candle):

        key = f"{candle.symbol}_{candle.interval}"

        if key not in self.previous_close:

            tr = candle.high - candle.low

        else:

            prev = self.previous_close[key]

            tr = max(

                candle.high - candle.low,

                abs(candle.high - prev),

                abs(candle.low - prev)

            )

        self.previous_close[key] = candle.close

        self.tr[key].append(Decimal(str(tr)))

        if len(self.tr[key]) < self.period:

            return None

        return sum(self.tr[key]) / Decimal(len(self.tr[key]))