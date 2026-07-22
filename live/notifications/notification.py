from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4


@dataclass(slots=True)
class Notification:

    notification_id: str = field(
        default_factory=lambda: uuid4().hex
    )

    channel: str = ""

    title: str = ""

    message: str = ""

    level: str = "INFO"

    metadata: dict = field(default_factory=dict)

    created_at: datetime = field(
        default_factory=datetime.utcnow
    )