from dataclasses import dataclass


@dataclass(slots=True)
class HeartbeatPolicy:

    enabled: bool = True

    timeout: float = 30.0

    interval: float = 5.0