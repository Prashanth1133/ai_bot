from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass(slots=True)
class FeatureRecord:

    timestamp: datetime

    symbol: str

    timeframe: str

    source: str

    features: dict[str, Any]
    