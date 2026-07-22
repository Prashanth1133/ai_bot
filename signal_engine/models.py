from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from enum import Enum


class SignalType(Enum):

    BUY = "BUY"

    SELL = "SELL"

    HOLD = "HOLD"


@dataclass(slots=True)
class TradingSignal:

    symbol: str

    timeframe: str

    signal: SignalType

    confidence: float

    entry: Decimal

    stop_loss: Decimal

    take_profit: Decimal

    reasons: list[str]