from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class StrategyContext:

    symbol: str

    timeframe: str

    features: dict = field(default_factory=dict)

    indicators: dict = field(default_factory=dict)

    smart_money: dict = field(default_factory=dict)

    regime: dict = field(default_factory=dict)

    sentiment: dict = field(default_factory=dict)

    portfolio: dict = field(default_factory=dict)