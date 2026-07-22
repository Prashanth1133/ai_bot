from __future__ import annotations

from decimal import Decimal

from live.risk.models import (

    MarketState,

    RiskViolation,

    RiskSeverity,

)


class VolatilityGuard:

    def __init__(

        self,

        minimum: Decimal,

        maximum: Decimal,

    ):

        self.minimum = minimum

        self.maximum = maximum

    def check(

        self,

        market: MarketState,

    ):

        volatility = market.volatility

        if volatility < self.minimum:

            return RiskViolation(

                source="VolatilityGuard",

                severity=RiskSeverity.MEDIUM,

                message="Volatility too low",

            )

        if volatility > self.maximum:

            return RiskViolation(

                source="VolatilityGuard",

                severity=RiskSeverity.HIGH,

                message="Volatility too high",

            )

        return None