from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4


@dataclass(slots=True)
class AuditEvent:

    event_id: str = field(
        default_factory=lambda: uuid4().hex
    )

    category: str = ""

    action: str = ""

    component: str = ""

    user: str = "system"

    success: bool = True

    message: str = ""

    metadata: dict = field(default_factory=dict)

    timestamp: datetime = field(
        default_factory=datetime.utcnow
    )