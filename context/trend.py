from enum import Enum


class Trend(Enum):

    STRONG_BULLISH = 2

    BULLISH = 1

    NEUTRAL = 0

    BEARISH = -1

    STRONG_BEARISH = -2


class TrendAnalyzer:

    def analyze(self, ema20, ema50, ema200):

        if ema20 > ema50 > ema200:

            return Trend.STRONG_BULLISH

        if ema20 > ema50:

            return Trend.BULLISH

        if ema20 < ema50 < ema200:

            return Trend.STRONG_BEARISH

        if ema20 < ema50:

            return Trend.BEARISH

        return Trend.NEUTRAL