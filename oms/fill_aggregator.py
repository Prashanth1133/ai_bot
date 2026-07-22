from __future__ import annotations

from decimal import Decimal


class FillAggregator:

    def aggregate(
        self,
        fills,
    ):

        if not fills:
            return None

        qty = Decimal("0")
        value = Decimal("0")
        fee = Decimal("0")

        for fill in fills:

            qty += fill.quantity
            value += fill.quantity * fill.price
            fee += fill.commission

        avg = Decimal("0")

        if qty > 0:
            avg = value / qty

        return {

            "quantity": qty,

            "average_price": avg,

            "commission": fee,
        }