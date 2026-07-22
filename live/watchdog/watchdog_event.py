from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass(slots=True)
class WatchdogEvent:

    component: str

    status: str

    message: str = ""

    timestamp: datetime = field(
        default_factory=datetime.utcnow
    )