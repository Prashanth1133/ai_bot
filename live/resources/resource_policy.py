from dataclasses import dataclass


@dataclass(slots=True)
class ResourcePolicy:

    cpu_limit: float = 90.0

    memory_limit_mb: float = 8192.0

    disk_limit: float = 90.0

    monitoring_interval: float = 2.0