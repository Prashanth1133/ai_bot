from dataclasses import dataclass


@dataclass(slots=True)
class AuditPolicy:

    enabled: bool = True

    persist: bool = True

    max_records: int = 1000000

    export_interval: int = 300