from __future__ import annotations

from collections import defaultdict
from decimal import Decimal


class FillManager:

    def __init__(self):

        self._fills = defaultdict(list)

    def add_fill(
        self,
        order_id: str,
        quantity: Decimal,
        price: Decimal,
        commission: Decimal = Decimal("0"),
    ):

        self._fills[order_id].append(
            {
                "qty": quantity,
                "price": price,
                "commission": commission,
            }
        )

    def fills(self, order_id: str):

        return list(self._fills.get(order_id, []))

    def total_quantity(
        self,
        order_id: str,
    ):

        return sum(
            f["qty"]
            for f in self._fills.get(order_id, [])
        )

    def average_price(
        self,
        order_id: str,
    ):

        fills = self._fills.get(order_id, [])

        if not fills:
            return Decimal("0")

        qty = sum(f["qty"] for f in fills)

        if qty == 0:
            return Decimal("0")

        value = sum(
            f["qty"] * f["price"]
            for f in fills
        )

        return value / qty

    def clear(self, order_id: str):

        self._fills.pop(order_id, None)