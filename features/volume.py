from __future__ import annotations

from collections import deque
from decimal import Decimal
from dataclasses import dataclass

from models.market import Trade


@dataclass(slots=True)
class OrderFlowMetrics:

    buy_volume: Decimal = Decimal("0")

    sell_volume: Decimal = Decimal("0")

    delta: Decimal = Decimal("0")

    cvd: Decimal = Decimal("0")

    trades: int = 0

    aggressive_buyers: int = 0

    aggressive_sellers: int = 0