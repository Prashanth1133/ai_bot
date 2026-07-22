from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class Position:

    symbol: str

    side: str

    quantity: float

    entry_price: float

    current_price: float

    stop_loss: float

    take_profit: float

    opened: datetime

    unrealized_pnl: float = 0.0