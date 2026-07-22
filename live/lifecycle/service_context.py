from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass(slots=True)
class ServiceContext:

    name: str

    state: str = "CREATED"

    started_at: datetime | None = None

    stopped_at: datetime | None = None

    restart_count: int = 0

    metadata: dict = field(default_factory=dict)