from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass(slots=True)
class SystemSnapshot:

    timestamp: datetime = field(
        default_factory=datetime.utcnow
    )

    state: str = ""

    cpu_usage: float = 0.0

    memory_usage: float = 0.0

    active_services: int = 0

    active_symbols: int = 0

    metadata: dict = field(
        default_factory=dict
    )