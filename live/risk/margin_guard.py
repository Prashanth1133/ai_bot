from __future__ import annotations

from decimal import Decimal

from live.risk.models import (
    PortfolioState,
    TradeRequest,
    RiskViolation,
    RiskSeverity,
)


class MarginGuard:

    def __init__(

        self,

        minimum_margin_ratio: Decimal,

    ):

        self.minimum_margin_ratio = minimum_margin_ratio

    def check(

        self,

        trade: TradeRequest,

        portfolio: PortfolioState,

    ) -> RiskViolation | None:

        if portfolio.equity <= 0:

            return None

        required = (

            trade.entry_price

            * trade.quantity

        ) / trade.leverage

        ratio = (

            portfolio.free_margin

            - required

        ) / portfolio.equity

        if ratio < self.minimum_margin_ratio:

            return RiskViolation(

                source="MarginGuard",

                severity=RiskSeverity.CRITICAL,

                message="Insufficient free margin",

            )

        return None