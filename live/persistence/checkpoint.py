from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass(slots=True)
class Checkpoint:

    name: str

    state: dict

    timestamp: datetime = field(
        default_factory=datetime.utcnow
    )