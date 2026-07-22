from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass(slots=True)
class DiagnosticResult:

    component: str

    passed: bool

    message: str = ""

    details: dict = field(default_factory=dict)

    timestamp: datetime = field(
        default_factory=datetime.utcnow
    )