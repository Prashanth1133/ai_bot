from decimal import Decimal


class VWAPCalculator:

    def calculate(self, candles):

        pv = Decimal("0")

        volume = Decimal("0")

        for candle in candles:

            typical = (

                candle.high +

                candle.low +

                candle.close

            ) / Decimal("3")

            pv += typical * candle.volume

            volume += candle.volume

        if volume == 0:

            return None

        return pv / volume