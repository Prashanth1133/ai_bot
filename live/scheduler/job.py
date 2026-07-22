from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4
from typing import Callable


@dataclass(slots=True)
class Job:

    id: str = field(default_factory=lambda: uuid4().hex)

    name: str = ""

    callback: Callable | None = None

    interval: float = 1.0

    enabled: bool = True

    last_run: datetime | None = None

    next_run: datetime | None = None

    metadata: dict = field(default_factory=dict)