from volume_profile.profile import (
    VolumeProfileCalculator
)

from volume_profile.vwap import (
    VWAPCalculator
)


class VolumeProfileEngine:

    def __init__(self):

        self.profile = VolumeProfileCalculator()

        self.vwap = VWAPCalculator()

    def process(self, candles):

        profile = self.profile.calculate(

            candles

        )

        vwap = self.vwap.calculate(

            candles

        )

        return {

            "profile": profile,

            "vwap": vwap

        }