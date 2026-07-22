from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4


@dataclass(slots=True)
class OMSSession:

    session_id: str = field(
        default_factory=lambda: uuid4().hex
    )

    started_at: datetime = field(
        default_factory=datetime.utcnow
    )

    exchange: str = ""

    account: str = ""

    mode: str = "LIVE"