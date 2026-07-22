from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal


@dataclass(slots=True)
class RiskMetrics:

    equity: Decimal = Decimal("0")

    balance: Decimal = Decimal("0")

    used_margin: Decimal = Decimal("0")

    free_margin: Decimal = Decimal("0")

    leverage: Decimal = Decimal("0")

    exposure: Decimal = Decimal("0")

    drawdown: Decimal = Decimal("0")

    unrealized_pnl: Decimal = Decimal("0")

    realized_pnl: Decimal = Decimal("0")

    win_rate: Decimal = Decimal("0")

    profit_factor: Decimal = Decimal("0")