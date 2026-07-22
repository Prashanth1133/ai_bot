from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class DatasetMetadata:

    dataset_name: str

    symbol: str

    timeframe: str

    rows: int

    features: int

    created_at: datetime

    version: str = "1.0"