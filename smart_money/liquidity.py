from decimal import Decimal

from smart_money.liquidity_zone import (
    LiquidityZone,
    LiquidityType
)


class LiquidityDetector:

    """
    Detect Equal Highs / Equal Lows
    """

    def __init__(

        self,

        tolerance=Decimal("0.001")

    ):

        self.tolerance = tolerance

    def detect(

        self,

        candles

    ):

        zones = []

        if len(candles) < 8:

            return zones

        highs = {}

        lows = {}

        for candle in candles[-50:]:

            rounded_high = candle.high.quantize(
                Decimal("0.1")
            )

            rounded_low = candle.low.quantize(
                Decimal("0.1")
            )

            highs.setdefault(
                rounded_high,
                []
            ).append(candle)

            lows.setdefault(
                rounded_low,
                []
            ).append(candle)

        for level, group in highs.items():

            if len(group) >= 2:

                zones.append(

                    LiquidityZone(

                        symbol=group[-1].symbol,

                        timeframe=group[-1].interval,

                        level=level,

                        touches=len(group),

                        zone_type=LiquidityType.BUY_SIDE,

                        created_at=group[-1].close_time,

                        strength=min(

                            len(group) / 5,

                            1.0

                        )

                    )

                )

        for level, group in lows.items():

            if len(group) >= 2:

                zones.append(

                    LiquidityZone(

                        symbol=group[-1].symbol,

                        timeframe=group[-1].interval,

                        level=level,

                        touches=len(group),

                        zone_type=LiquidityType.SELL_SIDE,

                        created_at=group[-1].close_time,

                        strength=min(

                            len(group) / 5,

                            1.0

                        )

                    )

                )

        return zones