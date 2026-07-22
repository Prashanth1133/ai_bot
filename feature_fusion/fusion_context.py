from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class FusionContext:

    symbol: str

    timeframe: str

    timestamp: int

    features: dict = field(default_factory=dict)

    metadata: dict = field(default_factory=dict)