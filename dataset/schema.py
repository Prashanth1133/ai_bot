from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class DatasetSchema:

    version: str = "1.0"

    symbol: str = ""

    timeframe: str = ""

    sequence_length: int = 128

    prediction_horizon: int = 24

    feature_names: list[str] = field(default_factory=list)

    label_names: list[str] = field(default_factory=list)

    metadata: dict[str, Any] = field(default_factory=dict)