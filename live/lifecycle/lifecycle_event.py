from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass(slots=True)
class LifecycleEvent:

    component: str

    previous_state: str

    current_state: str

    timestamp: datetime = field(
        default_factory=datetime.utcnow
    )

    metadata: dict = field(
        default_factory=dict
    )