from dataclasses import dataclass


@dataclass(slots=True)
class CachePolicy:

    default_ttl: float = 300.0

    cleanup_interval: float = 60.0

    max_entries: int = 100000