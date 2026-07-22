from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Awaitable, Callable


@dataclass(slots=True)
class ScheduledTask:

    name: str

    coroutine: Callable[..., Awaitable]

    interval: float

    enabled: bool = True

    last_run: datetime | None = None

    next_run: datetime | None = None

    metadata: dict = field(default_factory=dict)