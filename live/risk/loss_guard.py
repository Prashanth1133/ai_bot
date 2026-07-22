from __future__ import annotations

from decimal import Decimal
from datetime import date

from live.risk.models import (
    PortfolioState,
    RiskSeverity,
    RiskViolation,
)


class LossGuard:

    def __init__(

        self,

        daily_limit: Decimal,

        weekly_limit: Decimal,

    ):

        self.daily_limit = daily_limit

        self.weekly_limit = weekly_limit

        self.current_day = date.today()

        self.daily_loss = Decimal("0")

        self.weekly_loss = Decimal("0")

    def update(

        self,

        pnl: Decimal,

    ):

        today = date.today()

        if today != self.current_day:

            self.daily_loss = Decimal("0")

            self.current_day = today

        if pnl < 0:

            self.daily_loss += abs(pnl)

            self.weekly_loss += abs(pnl)

    def check(

        self,

        portfolio: PortfolioState,

    ) -> RiskViolation | None:

        if portfolio.balance == 0:

            return None

        daily = self.daily_loss / portfolio.balance

        weekly = self.weekly_loss / portfolio.balance

        if daily >= self.daily_limit:

            return RiskViolation(

                source="LossGuard",

                severity=RiskSeverity.CRITICAL,

                message="Daily loss limit exceeded",

            )

        if weekly >= self.weekly_limit:

            return RiskViolation(

                source="LossGuard",

                severity=RiskSeverity.CRITICAL,

                message="Weekly loss limit exceeded",

            )

        return None