from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass(slots=True)
class Statistic:

    name: str

    value: float = 0.0

    unit: str = ""

    metadata: dict = field(default_factory=dict)

    updated_at: datetime = field(
        default_factory=datetime.utcnow
    )