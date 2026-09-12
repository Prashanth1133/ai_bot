from __future__ import annotations

from dataclasses import dataclass, field
from feature_fusion.schema import UNIFIED_FEATURE_SCHEMA, NUM_UNIFIED_FEATURES

DEFAULT_LABEL_NAMES = [
    "direction",
    "reversal",
    "regime",
    "future_return_15m",
    "future_return_30m",
    "future_return_1h",
    "future_return_4h",
    "max_future_return_15m",
    "min_future_return_15m",
    "max_future_return_1h",
    "min_future_return_1h",
    "max_future_return_4h",
    "min_future_return_4h",
    "take_profits",
    "stop_losses",
    "future_high",
    "future_low",
]


@dataclass(slots=True)
class DatasetSchema:
    version: str = "FINAL-1M-MTF-V5"
    symbol: str = "BTCUSDT"
    base_timeframe: str = "1m"
    sequence_length: int = 128
    timeframes: list[str] = field(default_factory=lambda: ["1m", "5m", "15m", "1h", "4h"])
    feature_names: list[str] = field(default_factory=lambda: list(UNIFIED_FEATURE_SCHEMA))
    label_names: list[str] = field(default_factory=lambda: list(DEFAULT_LABEL_NAMES))
    metadata: dict[str, str] = field(default_factory=dict)