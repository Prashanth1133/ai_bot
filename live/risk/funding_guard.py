from __future__ import annotations

from decimal import Decimal

from live.risk.models import (
    MarketState,
    RiskSeverity,
    RiskViolation,
)


class FundingGuard:
    """
    Reject trades when funding becomes extreme.
    """

    def __init__(
        self,
        max_positive: Decimal,
        max_negative: Decimal,
    ):
        self.max_positive = max_positive
        self.max_negative = max_negative

    def check(
        self,
        market: MarketState,
    ) -> RiskViolation | None:

        funding = market.funding_rate

        if funding >= self.max_positive:

            return RiskViolation(
                source="FundingGuard",
                severity=RiskSeverity.HIGH,
                message=(
                    f"Funding rate too high ({funding:.4%})"
                ),
            )

        if funding <= self.max_negative:

            return RiskViolation(
                source="FundingGuard",
                severity=RiskSeverity.HIGH,
                message=(
                    f"Funding rate too low ({funding:.4%})"
                ),
            )

        return None