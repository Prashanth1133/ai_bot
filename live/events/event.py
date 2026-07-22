from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4


@dataclass(slots=True)
class LiveEvent:

    event_id: str = field(
        default_factory=lambda: uuid4().hex
    )

    event_type: str = ""

    source: str = ""

    payload: dict = field(default_factory=dict)

    timestamp: datetime = field(
        default_factory=datetime.utcnow
    )