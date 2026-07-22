from enum import Enum


class MarketRegime(Enum):

    TREND = "trend"

    RANGE = "range"

    VOLATILE = "volatile"

    QUIET = "quiet"


class RegimeDetector:

    def detect(

        self,

        features,

    ):

        adx = features["adx"]

        atr = features["atr"]

        if adx > 25:

            return MarketRegime.TREND

        if atr > features["atr_mean"] * 1.5:

            return MarketRegime.VOLATILE

        return MarketRegime.RANGE