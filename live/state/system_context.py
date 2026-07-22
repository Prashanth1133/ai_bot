from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass(slots=True)
class SystemContext:

    state: str = "INITIALIZING"

    started_at: datetime | None = None

    stopped_at: datetime | None = None

    version: str = "1.0.0"

    metadata: dict = field(default_factory=dict)