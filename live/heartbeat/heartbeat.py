from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass(slots=True)
class Heartbeat:

    component: str

    healthy: bool = True

    message: str = ""

    timestamp: datetime = field(
        default_factory=datetime.utcnow
    )