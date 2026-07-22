from dataclasses import dataclass, field
from datetime import datetime


@dataclass(slots=True)
class ServiceHealth:

    service: str

    healthy: bool = True

    message: str = ""

    checked_at: datetime = field(
        default_factory=datetime.utcnow
    )