from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from typing import Dict, List, Optional


@dataclass(slots=True)
class TradeRecord:
    trade_id: str
    order_id: str
    symbol: str
    side: str
    quantity: Decimal
    price: Decimal
    commission: Decimal = Decimal("0")
    realized_pnl: Decimal = Decimal("0")
    timestamp: datetime = field(default_factory=datetime.utcnow)
    metadata: Dict = field(default_factory=dict)


class TradeRegistry:

    def __init__(self):
        self._trades: Dict[str, TradeRecord] = {}
        self._symbol_index: Dict[str, List[str]] = {}

    def add(self, trade: TradeRecord):

        self._trades[trade.trade_id] = trade

        self._symbol_index.setdefault(
            trade.symbol,
            []
        ).append(trade.trade_id)

    def exists(self, trade_id: str) -> bool:
        return trade_id in self._trades

    def get(self, trade_id: str) -> Optional[TradeRecord]:
        return self._trades.get(trade_id)

    def by_symbol(self, symbol: str):
        ids = self._symbol_index.get(symbol, [])
        return [self._trades[i] for i in ids]

    def all(self):
        return list(self._trades.values())

    def remove(self, trade_id: str):

        trade = self._trades.pop(trade_id, None)

        if trade is None:
            return

        self._symbol_index.get(
            trade.symbol,
            []
        ).remove(trade_id)

    def clear(self):
        self._trades.clear()
        self._symbol_index.clear()