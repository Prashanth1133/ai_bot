from __future__ import annotations

from decimal import Decimal

from live.risk.models import (
    MarketState,
    RiskSeverity,
    RiskViolation,
)


class OpenInterestGuard:
    """
    Detect abnormal OI expansion.
    """

    def __init__(
        self,
        max_change: Decimal,
    ):
        self.max_change = max_change

    def check(
        self,
        current_oi: Decimal,
        previous_oi: Decimal,
    ) -> RiskViolation | None:

        if previous_oi <= 0:
            return None

        change = (
            current_oi
            - previous_oi
        ) / previous_oi

        if abs(change) >= self.max_change:

            return RiskViolation(
                source="OpenInterestGuard",
                severity=RiskSeverity.MEDIUM,
                message=(
                    f"Open Interest changed "
                    f"{change:.2%}"
                ),
            )

        return None