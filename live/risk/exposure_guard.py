from __future__ import annotations

from decimal import Decimal

from live.risk.models import (
    PortfolioState,
    TradeRequest,
    RiskViolation,
    RiskSeverity,
)


class ExposureGuard:

    """
    Prevent excessive portfolio concentration.
    """

    def __init__(

        self,

        max_symbol_exposure: Decimal,

        max_total_exposure: Decimal,

    ):

        self.max_symbol = max_symbol_exposure

        self.max_total = max_total_exposure

    def check(

        self,

        trade: TradeRequest,

        portfolio: PortfolioState,

    ) -> RiskViolation | None:

        equity = portfolio.equity

        if equity <= 0:

            return None

        symbol_value = Decimal("0")

        total_value = Decimal("0")

        for position in portfolio.positions:

            value = (

                position.entry_price

                * position.quantity

            )

            total_value += value

            if position.symbol == trade.symbol:

                symbol_value += value

        proposed = (

            trade.entry_price

            * trade.quantity

        )

        symbol_ratio = (

            symbol_value + proposed

        ) / equity

        total_ratio = (

            total_value + proposed

        ) / equity

        if symbol_ratio > self.max_symbol:

            return RiskViolation(

                source="ExposureGuard",

                severity=RiskSeverity.HIGH,

                message=(
                    "Maximum symbol exposure exceeded"
                ),

            )

        if total_ratio > self.max_total:

            return RiskViolation(

                source="ExposureGuard",

                severity=RiskSeverity.CRITICAL,

                message=(
                    "Maximum portfolio exposure exceeded"
                ),

            )

        return None