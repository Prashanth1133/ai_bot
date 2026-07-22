from dataclasses import dataclass
from decimal import Decimal


@dataclass(slots=True)
class PortfolioSnapshot:

    equity: Decimal

    cash: Decimal

    unrealized_pnl: Decimal

    realized_pnl: Decimal

    exposure: Decimal

    margin_used: Decimal

    free_margin: Decimal