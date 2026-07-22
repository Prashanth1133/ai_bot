from __future__ import annotations

from decimal import Decimal

from live.risk.models import (
    PortfolioState,
    RiskSeverity,
    RiskViolation,
)


class DrawdownGuard:

    def __init__(

        self,

        max_drawdown: Decimal,

    ):

        self.max_drawdown = max_drawdown

        self.peak_equity = Decimal("0")

    def check(

        self,

        portfolio: PortfolioState,

    ) -> RiskViolation | None:

        if portfolio.equity > self.peak_equity:

            self.peak_equity = portfolio.equity

            return None

        if self.peak_equity == 0:

            return None

        drawdown = (

            self.peak_equity

            - portfolio.equity

        ) / self.peak_equity

        if drawdown >= self.max_drawdown:

            return RiskViolation(

                source="DrawdownGuard",

                severity=RiskSeverity.CRITICAL,

                message=f"Maximum drawdown exceeded ({drawdown:.2%})",

            )

        return None