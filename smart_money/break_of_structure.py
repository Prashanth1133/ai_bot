from enum import Enum


class BOS(Enum):

    NONE = 0

    BULLISH = 1

    BEARISH = -1


class BreakOfStructure:

    """
    Detects Break Of Structure
    """

    def detect(self, structure):

        if structure.name == "HH":

            return BOS.BULLISH

        if structure.name == "LL":

            return BOS.BEARISH

        return BOS.NONE