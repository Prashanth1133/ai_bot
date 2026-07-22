from collections import defaultdict

from smart_money.fvg_types import (
    FVGStatus,
)


class FVGManager:

    def __init__(self):

        self.gaps = defaultdict(list)

    def add(self, gap):

        self.gaps[gap.symbol].append(gap)

    def update(self, symbol, price):

        for gap in self.gaps[symbol]:

            if gap.status != FVGStatus.OPEN:
                continue

            if gap.lower <= price <= gap.upper:

                gap.status = FVGStatus.FILLED

    def active(self, symbol):

        return [

            gap

            for gap in self.gaps[symbol]

            if gap.status == FVGStatus.OPEN

        ]