from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class AccountSnapshot:

    equity: float

    balance: float

    margin: float

    free_margin: float

    timestamp: datetime