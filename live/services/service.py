from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from live.services.service_state import ServiceState


@dataclass(slots=True)
class Service:

    name: str

    state: ServiceState = ServiceState.CREATED

    started_at: datetime | None = None

    stopped_at: datetime | None = None

    metadata: dict = field(default_factory=dict)