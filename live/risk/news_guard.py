from __future__ import annotations

from live.risk.models import (
    MarketState,
    RiskViolation,
    RiskSeverity,
)


class NewsGuard:

    def __init__(

        self,

        threshold: float,

    ):

        self.threshold = threshold

    def check(

        self,

        market: MarketState,

    ):

        if market.news_score >= self.threshold:

            return RiskViolation(

                source="NewsGuard",

                severity=RiskSeverity.HIGH,

                message="High impact news detected",

            )

        return None