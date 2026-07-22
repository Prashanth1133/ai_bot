from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal


@dataclass

class PaperOrder:

    symbol: str

    side: str

    quantity: Decimal

    price: Decimal

    stop_loss: Decimal

    take_profit: Decimal