from __future__ import annotations

from decimal import Decimal

from live.risk.models import (
    RiskViolation,
    RiskSeverity,
)


class CorrelationGuard:

    def __init__(

        self,

        threshold: Decimal,

    ):

        self.threshold = threshold

    def check(

        self,

        correlation: Decimal,

    ) -> RiskViolation | None:

        if correlation >= self.threshold:

            return RiskViolation(

                source="CorrelationGuard",

                severity=RiskSeverity.HIGH,

                message=(
                    f"Correlation too high "
                    f"({correlation:.2f})"
                ),

            )

        return None