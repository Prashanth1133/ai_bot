from collections import defaultdict
from decimal import Decimal

from volume_profile.models import VolumeProfile


class VolumeProfileCalculator:

    """
    Fixed-range Volume Profile
    """

    def __init__(self, bins=100):

        self.bins = bins

    def calculate(self, candles):

        histogram = defaultdict(Decimal)

        for candle in candles:

            price = candle.close.quantize(
                Decimal("0.10")
            )

            histogram[price] += candle.volume

        if not histogram:

            return None

        prices = sorted(histogram.keys())

        poc = max(
            histogram.items(),
            key=lambda x: x[1]
        )[0]

        total = sum(histogram.values())

        vah = prices[-1]

        val = prices[0]

        hvn = []

        lvn = []

        average = total / len(prices)

        for p, v in histogram.items():

            if v > average:

                hvn.append(p)

            else:

                lvn.append(p)

        return VolumeProfile(

            poc=poc,

            vah=vah,

            val=val,

            hvn=hvn,

            lvn=lvn,

            total_volume=total

        )