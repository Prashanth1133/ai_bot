from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal
from enum import Enum
from typing import List, Optional


class RiskStatus(Enum):

    APPROVED = "approved"

    REJECTED = "rejected"

    WARNING = "warning"


class RiskSeverity(Enum):

    LOW = "low"

    MEDIUM = "medium"

    HIGH = "high"

    CRITICAL = "critical"


@dataclass(slots=True)
class RiskViolation:

    source: str

    severity: RiskSeverity

    message: str


@dataclass(slots=True)
class TradeRequest:

    symbol: str

    side: str

    entry_price: Decimal

    quantity: Decimal

    stop_loss: Decimal

    take_profit: Decimal

    leverage: int = 1


@dataclass(slots=True)
class PortfolioState:

    equity: Decimal

    balance: Decimal

    used_margin: Decimal

    free_margin: Decimal

    unrealized_pnl: Decimal

    realized_pnl: Decimal

    positions: list = field(default_factory=list)


@dataclass(slots=True)
class MarketState:

    atr: Decimal

    spread: Decimal

    funding_rate: Decimal

    open_interest: Decimal

    volatility: Decimal

    bid_liquidity: Decimal

    ask_liquidity: Decimal

    news_score: float

    sentiment_score: float


@dataclass(slots=True)
class RiskDecision:

    status: RiskStatus

    approved: bool

    violations: List[RiskViolation]

    adjusted_quantity: Optional[Decimal] = None

    adjusted_stop: Optional[Decimal] = None

    adjusted_target: Optional[Decimal] = None