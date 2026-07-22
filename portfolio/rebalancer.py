from __future__ import annotations

from decimal import Decimal


class PortfolioRebalancer:

    def rebalance(
        self,
        current: dict[str, Decimal],
        target: dict[str, Decimal],
    ):

        orders = []

        symbols = (
            set(current.keys())
            | set(target.keys())
        )

        for symbol in symbols:

            current_weight = current.get(
                symbol,
                Decimal("0"),
            )

            target_weight = target.get(
                symbol,
                Decimal("0"),
            )

            delta = (
                target_weight
                - current_weight
            )

            if delta == 0:
                continue

            orders.append(
                {
                    "symbol": symbol,
                    "adjustment": delta,
                }
            )

        return orders