from __future__ import annotations

from decimal import Decimal

from live.risk.models import (
    PortfolioState,
    TradeRequest,
    RiskViolation,
    RiskSeverity,
)


class PositionLimits:

    """
    Checks per-position limits.
    """

    def __init__(

        self,

        max_position_percent: Decimal,

        max_leverage: int,

    ):

        self.max_position_percent = max_position_percent

        self.max_leverage = max_leverage

    def check(

        self,

        trade: TradeRequest,

        portfolio: PortfolioState,

    ) -> RiskViolation | None:

        if portfolio.equity <= 0:

            return RiskViolation(

                source="PositionLimits",

                severity=RiskSeverity.CRITICAL,

                message="Invalid portfolio equity",

            )

        position_value = (

            trade.entry_price

            * trade.quantity

        )

        ratio = (

            position_value

            / portfolio.equity

        )

        if ratio > self.max_position_percent:

            return RiskViolation(

                source="PositionLimits",

                severity=RiskSeverity.HIGH,

                message=(
                    f"Position exceeds "
                    f"{self.max_position_percent:.0%}"
                ),

            )

        if trade.leverage > self.max_leverage:

            return RiskViolation(

                source="PositionLimits",

                severity=RiskSeverity.CRITICAL,

                message=(
                    f"Leverage "
                    f"{trade.leverage}x exceeds "
                    f"{self.max_leverage}x"
                ),

            )

        return None