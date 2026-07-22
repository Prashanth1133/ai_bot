from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class Allocation:

    symbol: str

    target_weight: float

    current_weight: float = 0.0

    capital: float = 0.0

    leverage: float = 1.0

    metadata: dict = field(default_factory=dict)