from dataclasses import dataclass


@dataclass(slots=True)
class TelemetryPolicy:

    enabled: bool = True

    retention: int = 50000

    export_interval: int = 300

    compression: bool = False