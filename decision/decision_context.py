from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict


@dataclass(slots=True)
class DecisionContext:

    symbol: str

    strategy_result: Any

    ai_prediction: Any

    risk_result: Any

    portfolio_state: Dict[str, Any] = field(default_factory=dict)

    metadata: Dict[str, Any] = field(default_factory=dict)

    timestamp: datetime = field(default_factory=datetime.utcnow)