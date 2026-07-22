from __future__ import annotations

from decimal import Decimal
from dataclasses import dataclass


@dataclass(slots=True)
class TakeProfitLevel:

    price: Decimal

    percentage: Decimal


class TakeProfitCalculator:

    def __init__(

        self,

        rr_levels=None,

    ):

        self.rr = rr_levels or [

            Decimal("1"),

            Decimal("2"),

            Decimal("3"),

            Decimal("5"),

        ]

    def calculate(

        self,

        entry: Decimal,

        stop: Decimal,

        long: bool,

    ):

        risk = abs(

            entry - stop

        )

        targets = []

        for rr in self.rr:

            if long:

                price = entry + risk * rr

            else:

                price = entry - risk * rr

            targets.append(

                TakeProfitLevel(

                    price=price,

                    percentage=Decimal("0.25"),

                )

            )

        return targets