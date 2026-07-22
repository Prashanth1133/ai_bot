from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4


@dataclass(slots=True)
class RecoveryTask:

    task_id: str = field(
        default_factory=lambda: uuid4().hex
    )

    component: str = ""

    action: str = ""

    priority: int = 100

    retries: int = 0

    metadata: dict = field(default_factory=dict)

    created_at: datetime = field(
        default_factory=datetime.utcnow
    )