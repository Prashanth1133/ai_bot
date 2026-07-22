from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass(slots=True)
class RecoveryContext:

    component: str

    state: str = "IDLE"

    attempts: int = 0

    last_error: str = ""

    last_recovery: datetime | None = None

    metadata: dict = field(default_factory=dict)