from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass(slots=True)
class Resource:

    name: str

    cpu_percent: float = 0.0

    memory_mb: float = 0.0

    disk_percent: float = 0.0

    network_in: float = 0.0

    network_out: float = 0.0

    timestamp: datetime = field(
        default_factory=datetime.utcnow
    )