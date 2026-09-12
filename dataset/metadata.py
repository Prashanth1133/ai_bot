from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass(slots=True)
class DatasetMetadata:
    dataset_name: str
    symbol: str
    base_timeframe: str
    total_samples: int
    train_samples: int
    val_samples: int
    test_samples: int
    sequence_length: int
    feature_dim: int
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    dataset_version: str = "FINAL-1M-MTF-V5"
    feature_version: str = "FEATURES-1M-V5"
    label_version: str = "LABELS-PATH-MULTI-HORIZON"
    timeframes: list[str] = field(default_factory=lambda: ["1m", "5m", "15m", "1h", "4h"])
    prediction_horizons: list[int] = field(default_factory=lambda: [15, 30, 60, 240])