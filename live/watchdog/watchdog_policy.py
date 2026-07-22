from dataclasses import dataclass


@dataclass(slots=True)
class WatchdogPolicy:

    enabled: bool = True

    interval: float = 5.0

    restart_on_failure: bool = True

    max_failures: int = 3