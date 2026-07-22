from smart_money.fvg_types import (
    FairValueGap,
    FVGType,
)


class FairValueGapDetector:

    """
    Detects 3-candle Fair Value Gaps.
    """

    def detect(self, candles):

        gaps = []

        if len(candles) < 3:
            return gaps

        for i in range(2, len(candles)):

            first = candles[i - 2]

            middle = candles[i - 1]

            last = candles[i]

            # Bullish FVG
            if first.high < last.low:

                gap = FairValueGap(

                    symbol=last.symbol,

                    timeframe=last.interval,

                    gap_type=FVGType.BULLISH,

                    upper=last.low,

                    lower=first.high,

                    created_at=last.close_time,

                    strength=float(
                        last.low - first.high
                    )

                )

                gaps.append(gap)

            # Bearish FVG
            elif first.low > last.high:

                gap = FairValueGap(

                    symbol=last.symbol,

                    timeframe=last.interval,

                    gap_type=FVGType.BEARISH,

                    upper=first.low,

                    lower=last.high,

                    created_at=last.close_time,

                    strength=float(
                        first.low - last.high
                    )

                )

                gaps.append(gap)

        return gaps