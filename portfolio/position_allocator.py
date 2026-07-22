from __future__ import annotations

from decimal import Decimal


class PositionAllocator:

    def allocate(

        self,

        signals,

        capital: Decimal,

    ):

        if not signals:

            return {}

        weight = capital / Decimal(
            len(signals)
        )

        allocation = {}

        for signal in signals:

            allocation[
                signal.symbol
            ] = weight

        return allocation