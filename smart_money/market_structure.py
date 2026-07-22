
from enum import Enum


class Structure(Enum):
    HH = "Higher High"
    HL = "Higher Low"
    LH = "Lower High"
    LL = "Lower Low"
    UNKNOWN = "Unknown"


class MarketStructure:
    """
    Converts swing points into market structure.
    """

    def analyze(self, swings):
        """
        Determine market structure from the last two swing points.

        Expected swing object:
            swing.price
            swing.is_high
        """

        if len(swings) < 2:
            return Structure.UNKNOWN

        previous = swings[-2]
        current = swings[-1]

        # Highs
        if current.is_high:
            if current.price > previous.price:
                return Structure.HH
            return Structure.LH

        # Lows
        if current.price > previous.price:
            return Structure.HL

        return Structure.LL

