from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta


@dataclass(slots=True)
class CacheEntry:

    key: str

    value: object

    ttl: float | None = None

    created_at: datetime = field(
        default_factory=datetime.utcnow
    )

    def expired(self) -> bool:

        if self.ttl is None:

            return False

        return (
            datetime.utcnow()
            >= self.created_at
            + timedelta(seconds=self.ttl)
        )