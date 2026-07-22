from __future__ import annotations

from decimal import Decimal

from live.risk.models import (
    MarketState,
    TradeRequest,
    RiskSeverity,
    RiskViolation,
)


class LiquidityGuard:
    """
    Ensure enough depth exists
    before entering a position.
    """

    def __init__(
        self,
        minimum_depth: Decimal,
    ):
        self.minimum_depth = minimum_depth

    def check(
        self,
        trade: TradeRequest,
        market: MarketState,
    ) -> RiskViolation | None:

        required = (
            trade.entry_price
            * trade.quantity
        )

        available = min(
            market.bid_liquidity,
            market.ask_liquidity,
        )

        if available < required * self.minimum_depth:

            return RiskViolation(
                source="LiquidityGuard",
                severity=RiskSeverity.HIGH,
                message="Insufficient market depth",
            )

        return None