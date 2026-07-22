from dataclasses import dataclass


@dataclass(slots=True)
class LifecyclePolicy:

    auto_start: bool = True

    auto_restart: bool = True

    graceful_shutdown_timeout: float = 30.0

    startup_timeout: float = 60.0