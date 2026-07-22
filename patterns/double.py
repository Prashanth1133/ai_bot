from patterns.models import *

from patterns.candle_utils import *


class DoublePatternDetector:

    def detect(self, candles):

        if len(candles) < 2:

            return []

        a = candles[-2]

        b = candles[-1]

        patterns = []

        if bearish(a) and bullish(b):

            if b.close > a.open and b.open < a.close:

                patterns.append(

                    CandlePattern(

                        PatternName.ENGULFING_BULL,

                        PatternType.BULLISH,

                        0.85,

                        len(candles)-1

                    )

                )

        if bullish(a) and bearish(b):

            if b.open > a.close and b.close < a.open:

                patterns.append(

                    CandlePattern(

                        PatternName.ENGULFING_BEAR,

                        PatternType.BEARISH,

                        0.85,

                        len(candles)-1

                    )

                )

        return patterns