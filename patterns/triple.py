from patterns.models import *

from patterns.candle_utils import *


class TriplePatternDetector:

    def detect(self, candles):

        if len(candles) < 3:

            return []

        c1 = candles[-3]

        c2 = candles[-2]

        c3 = candles[-1]

        patterns = []

        if bullish(c1) and bullish(c2) and bullish(c3):

            patterns.append(

                CandlePattern(

                    PatternName.THREE_WHITE,

                    PatternType.BULLISH,

                    0.90,

                    len(candles)-1

                )

            )

        if bearish(c1) and bearish(c2) and bearish(c3):

            patterns.append(

                CandlePattern(

                    PatternName.THREE_BLACK,

                    PatternType.BEARISH,

                    0.90,

                    len(candles)-1

                )

            )

        return patterns