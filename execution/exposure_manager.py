from decimal import Decimal


class ExposureManager:

    def __init__(self):

        self.symbols = {}

    def update(

        self,

        symbol,

        value,

    ):

        self.symbols[symbol] = value

    def exposure(self):

        return sum(

            self.symbols.values(),

            Decimal("0"),

        )