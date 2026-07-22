from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from datetime import datetime
from typing import Optional


@dataclass(slots=True)
class ExchangeOrder:

    order_id: str

    client_order_id: str

    symbol: str

    side: str

    order_type: str

    quantity: Decimal

    price: Decimal

    stop_price: Optional[Decimal]

    status: str

    filled_quantity: Decimal

    average_price: Decimal

    timestamp: datetime


@dataclass(slots=True)
class ExchangeFill:

    trade_id: str

    order_id: str

    symbol: str

    side: str

    quantity: Decimal

    price: Decimal

    commission: Decimal

    commission_asset: str

    realized_pnl: Decimal

    timestamp: datetime


@dataclass(slots=True)
class ExchangePosition:

    symbol: str

    quantity: Decimal

    entry_price: Decimal

    mark_price: Decimal

    unrealized_pnl: Decimal

    leverage: int

    margin_type: str

    liquidation_price: Decimal


@dataclass(slots=True)
class ExchangeBalance:

    asset: str

    wallet_balance: Decimal

    available_balance: Decimal

    cross_wallet_balance: Decimal

    unrealized_pnl: Decimal


@dataclass(slots=True)
class ExchangeTicker:

    symbol: str

    bid: Decimal

    ask: Decimal

    last: Decimal

    volume: Decimal

    timestamp: datetime