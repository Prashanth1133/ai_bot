from __future__ import annotations

from decimal import Decimal


class DrawdownTracker:

    def __init__(self):

        self.peak = Decimal("0")

        self.max_drawdown = Decimal("0")

    def update(self, equity: Decimal):

        equity = Decimal(str(equity))

        if equity > self.peak:

            self.peak = equity

        if self.peak == 0:

            return Decimal("0")

        drawdown = (
            self.peak - equity
        ) / self.peak

        if drawdown > self.max_drawdown:

            self.max_drawdown = drawdown

        return drawdown