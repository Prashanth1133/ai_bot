from __future__ import annotations

from decimal import Decimal


class AssetAllocator:

    def allocate(

        self,

        assets,

        capital: Decimal,

    ):

        if not assets:

            return {}

        allocation = capital / Decimal(
            len(assets)
        )

        return {
            asset: allocation
            for asset in assets
        }