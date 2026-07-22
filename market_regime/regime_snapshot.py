from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from market_regime.regime_state import RegimeState


@dataclass(slots=True)
class RegimeSnapshot:

    symbol: str

    timeframe: str

    regime: RegimeState

    confidence: float

    probability: dict = field(default_factory=dict)

    features: dict = field(default_factory=dict)

    timestamp: datetime = field(
        default_factory=datetime.utcnow
    )