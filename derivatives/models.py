from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal


@dataclass(slots=True)
class DerivativesSnapshot:

    symbol: str

    funding_rate: Decimal

    open_interest: Decimal

    taker_buy_volume: Decimal

    taker_sell_volume: Decimal

    long_short_ratio: Decimal

    liquidation_buy: Decimal

    liquidation_sell: Decimal