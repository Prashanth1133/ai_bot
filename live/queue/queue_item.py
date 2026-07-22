from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4


@dataclass(slots=True)
class QueueItem:

    id: str = field(
        default_factory=lambda: uuid4().hex
    )

    topic: str = ""

    payload: object = None

    priority: int = 100

    created_at: datetime = field(
        default_factory=datetime.utcnow
    )