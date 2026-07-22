from __future__ import annotations

from decimal import Decimal


class BalanceManager:

    def __init__(self):

        self.assets = {}

    def update(
        self,
        asset,
        wallet,
        available,
    ):

        self.assets[asset] = {

            "wallet": Decimal(str(wallet)),

            "available": Decimal(
                str(available)
            ),
        }

    def wallet(
        self,
        asset,
    ):

        if asset not in self.assets:
            return Decimal("0")

        return self.assets[asset]["wallet"]

    def available(
        self,
        asset,
    ):

        if asset not in self.assets:
            return Decimal("0")

        return self.assets[asset]["available"]