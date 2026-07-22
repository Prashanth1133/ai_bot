from __future__ import annotations

from decimal import Decimal

from live.risk.models import (
    PortfolioState,
)


class PositionSizer:

    """
    ATR risk-based sizing.

    Risk per trade =
        account_equity × risk%
    """

    def __init__(

        self,

        risk_per_trade: Decimal,

    ):

        self.risk = risk_per_trade

    def calculate(

        self,

        portfolio: PortfolioState,

        entry: Decimal,

        stop: Decimal,

    ) -> Decimal:

        risk_capital = (

            portfolio.equity

            * self.risk

        )

        stop_distance = abs(

            entry - stop

        )

        if stop_distance <= 0:

            return Decimal("0")

        quantity = (

            risk_capital

            / stop_distance

        )

        return quantity.quantize(

            Decimal("0.000001")

        )