from enum import Enum


class CHOCH(Enum):

    NONE = 0
    BULLISH = 1
    BEARISH = -1


class ChangeOfCharacter:

    def __init__(self):
        self.previous = None

    def detect(self, structure):

        if structure is None:
            return CHOCH.NONE

        current_name = getattr(
            structure,
            "name",
            "UNKNOWN",
        )

        if current_name == "UNKNOWN":
            return CHOCH.NONE

        if self.previous is None:
            self.previous = structure
            return CHOCH.NONE

        previous_name = getattr(
            self.previous,
            "name",
            "UNKNOWN",
        )

        result = CHOCH.NONE

        bearish_transition = (
            previous_name in ("HH", "HL")
            and current_name in ("LH", "LL")
        )

        bullish_transition = (
            previous_name in ("LH", "LL")
            and current_name in ("HH", "HL")
        )

        if bearish_transition:
            result = CHOCH.BEARISH

        elif bullish_transition:
            result = CHOCH.BULLISH

        self.previous = structure

        return result

    def update(self, structure):
        return self.detect(structure)

    def reset(self):
        self.previous = None