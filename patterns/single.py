from patterns.models import *

from patterns.candle_utils import *


class SinglePatternDetector:

    def detect(self, candles):

        if not candles:

            return []

        c = candles[-1]

        patterns = []

        b = body(c)

        r = candle_range(c)

        uw = upper_wick(c)

        lw = lower_wick(c)

        if r == 0:

            return patterns

        body_ratio = b / r

        if body_ratio < 0.10:

            patterns.append(

                CandlePattern(

                    PatternName.DOJI,

                    PatternType.NONE,

                    0.60,

                    len(candles)-1

                )

            )

        if lw > b * 2 and uw < b:

            patterns.append(

                CandlePattern(

                    PatternName.HAMMER,

                    PatternType.BULLISH,

                    0.75,

                    len(candles)-1

                )

            )

        if uw > b * 2 and lw < b:

            patterns.append(

                CandlePattern(

                    PatternName.SHOOTING_STAR,

                    PatternType.BEARISH,

                    0.75,

                    len(candles)-1

                )

            )

        return patterns