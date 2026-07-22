from decimal import Decimal


class SymbolFilters:

    def __init__(self):

        self.filters = {}

    def register(
        self,
        symbol,
        info,
    ):

        self.filters[symbol] = info

    def get(
        self,
        symbol,
    ):

        return self.filters.get(symbol)

    def min_qty(
        self,
        symbol,
    ):

        data = self.filters.get(symbol)

        if data is None:
            return Decimal("0")

        return Decimal(
            str(
                data.get(
                    "minQty",
                    "0",
                )
            )
        )

    def tick_size(
        self,
        symbol,
    ):

        data = self.filters.get(symbol)

        if data is None:
            return Decimal("0")

        return Decimal(
            str(
                data.get(
                    "tickSize",
                    "0",
                )
            )
        )