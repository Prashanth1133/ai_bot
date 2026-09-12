from enum import Enum


class BOS(Enum):

    NONE = 0
    BULLISH = 1
    BEARISH = -1


class BreakOfStructure:

    def detect(
        self,
        candles=None,
        swings=None,
        structure=None,
    ) -> BOS:

        if not candles or len(candles) < 2:
            return BOS.NONE

        if not swings:
            return BOS.NONE

        latest = candles[-1]
        previous = candles[-2]

        current_close = float(
            latest.close
        )

        previous_close = float(
            previous.close
        )

        prior_highs = [
            float(s.price)
            for s in swings
            if (
                s.is_high
                and getattr(
                    s,
                    "candle",
                    None,
                ) is not latest
            )
        ]

        prior_lows = [
            float(s.price)
            for s in swings
            if (
                not s.is_high
                and getattr(
                    s,
                    "candle",
                    None,
                ) is not latest
            )
        ]

        if prior_highs:

            previous_swing_high = prior_highs[-1]

            if (
                previous_close
                <= previous_swing_high
                and current_close
                > previous_swing_high
            ):
                return BOS.BULLISH

        if prior_lows:

            previous_swing_low = prior_lows[-1]

            if (
                previous_close
                >= previous_swing_low
                and current_close
                < previous_swing_low
            ):
                return BOS.BEARISH

        return BOS.NONE

    def reset(self):
        pass