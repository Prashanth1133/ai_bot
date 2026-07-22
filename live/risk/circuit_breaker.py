from __future__ import annotations

from decimal import Decimal

from live.risk.models import (
    PortfolioState,
)


class CircuitBreaker:

    def __init__(

        self,

        max_intraday_loss: Decimal,

    ):

        self.max_loss = max_intraday_loss

        self.triggered = False

    def check(

        self,

        daily_loss: Decimal,

    ) -> bool:

        if daily_loss >= self.max_loss:

            self.triggered = True

        return self.triggered

    def reset(self):

        self.triggered = False