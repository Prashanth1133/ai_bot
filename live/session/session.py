from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4

from live.session.session_state import SessionState


@dataclass(slots=True)
class Session:

    session_id: str = field(
        default_factory=lambda: uuid4().hex
    )

    name: str = ""

    state: SessionState = SessionState.CREATED

    created_at: datetime = field(
        default_factory=datetime.utcnow
    )

    connected_at: datetime | None = None

    disconnected_at: datetime | None = None

    metadata: dict = field(default_factory=dict)