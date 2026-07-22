from collections import defaultdict

from smart_money.liquidity_zone import (
    LiquidityStatus
)


class LiquidityManager:

    def __init__(self):

        self.zones = defaultdict(list)

    def add(

        self,

        zone

    ):

        self.zones[zone.symbol].append(zone)

    def update(

        self,

        symbol,

        price

    ):

        for zone in self.zones[symbol]:

            if zone.status != LiquidityStatus.ACTIVE:

                continue

            if abs(price - zone.level) < 0.0001:

                zone.status = LiquidityStatus.SWEPT

    def active(

        self,

        symbol

    ):

        return [

            z

            for z in self.zones[symbol]

            if z.status == LiquidityStatus.ACTIVE

        ]