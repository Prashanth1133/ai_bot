from __future__ import annotations

from decimal import Decimal


class PortfolioAllocator:

    def equal_weight(
        self,
        symbols: list[str],
    ):

        if not symbols:
            return {}

        weight = Decimal("1") / Decimal(
            len(symbols)
        )

        return {
            symbol: weight
            for symbol in symbols
        }

    def fixed_weight(
        self,
        weights: dict[str, Decimal],
    ):

        total = sum(
            weights.values(),
            Decimal("0"),
        )

        if total == 0:
            return {}

        return {
            k: v / total
            for k, v in weights.items()
        }