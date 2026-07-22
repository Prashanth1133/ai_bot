from decimal import Decimal

from smart_money.order_block_types import (
    OrderBlock,
    OrderBlockType,
)


class OrderBlockDetector:

    """
    Detects institutional order blocks.
    """

    def __init__(

        self,

        impulse_multiplier=2.0

    ):

        self.multiplier = Decimal(str(impulse_multiplier))

    def detect(

        self,

        candles,

        atr

    ):

        if len(candles) < 3:

            return []

        detected = []

        previous = candles[-2]

        current = candles[-1]

        body = abs(

            current.close -

            current.open

        )

        if body < atr * self.multiplier:

            return detected

        # -----------------------

        # Bullish Order Block

        # -----------------------

        if (

            previous.close < previous.open

            and

            current.close > current.open

        ):

            detected.append(

                OrderBlock(

                    symbol=current.symbol,

                    timeframe=current.interval,

                    type=OrderBlockType.BULLISH,

                    high=previous.high,

                    low=previous.low,

                    created_at=current.close_time,

                    strength=1.0

                )

            )

        # -----------------------

        # Bearish Order Block

        # -----------------------

        if (

            previous.close > previous.open

            and

            current.close < current.open

        ):

            detected.append(

                OrderBlock(

                    symbol=current.symbol,

                    timeframe=current.interval,

                    type=OrderBlockType.BEARISH,

                    high=previous.high,

                    low=previous.low,

                    created_at=current.close_time,

                    strength=1.0

                )

            )

        return detected