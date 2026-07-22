from enum import Enum


class CHOCH(Enum):

    NONE = 0

    BULLISH = 1

    BEARISH = -1


class ChangeOfCharacter:

    """
    Detects change in market direction.
    """

    def __init__(self):

        self.previous = None

    def detect(self, structure):

        if self.previous is None:

            self.previous = structure

            return CHOCH.NONE

        result = CHOCH.NONE

        if self.previous.name in ("HH", "HL") and \
           structure.name in ("LH", "LL"):

            result = CHOCH.BEARISH

        elif self.previous.name in ("LH", "LL") and \
             structure.name in ("HH", "HL"):

            result = CHOCH.BULLISH

        self.previous = structure

        return result