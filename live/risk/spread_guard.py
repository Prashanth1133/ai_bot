from __future__ import annotations

from decimal import Decimal

from live.risk.models import (
    MarketState,
    RiskSeverity,
    RiskViolation,
)


class SpreadGuard:
    """
    Reject trading when spread
    becomes too wide.
    """

    def __init__(
        self,
        maximum_spread: Decimal,
    ):
        self.maximum_spread = maximum_spread

    def check(
        self,
        market: MarketState,
    ) -> RiskViolation | None:

        if market.spread > self.maximum_spread:

            return RiskViolation(
                source="SpreadGuard",
                severity=RiskSeverity.HIGH,
                message=(
                    f"Spread too wide "
                    f"({market.spread:.3%})"
                ),
            )

        return None