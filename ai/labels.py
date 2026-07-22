import numpy as np


class LabelGenerator:

    """
    Creates labels from candles.
    """

    @staticmethod
    def direction(
        close_now,
        close_future,
        threshold=0.003
    ):

        pct = (
            close_future -
            close_now
        ) / close_now

        if pct > threshold:
            return 2

        if pct < -threshold:
            return 0

        return 1

    @staticmethod
    def confidence(
        probability
    ):

        return float(
            probability
        )

    @staticmethod
    def reversal(
        current_trend,
        future_trend
    ):

        return int(
            current_trend != future_trend
        )

    @staticmethod
    def volatility(
        highs,
        lows
    ):

        return float(

            np.mean(

                np.array(highs) -
                np.array(lows)

            )

        )

    @staticmethod
    def take_profit(
        close,
        future_high
    ):

        return (

            future_high -
            close

        ) / close

    @staticmethod
    def stop_loss(
        close,
        future_low
    ):

        return abs(

            (
                future_low -
                close
            ) / close

        )

    @staticmethod
    def market_regime(
        trend,
        volatility,
        volume
    ):

        score = 0

        if trend > 0:
            score += 3

        if volatility > 0.02:
            score += 3

        if volume > 1:
            score += 3

        return min(
            score,
            9
        )