from dataclasses import dataclass


@dataclass(slots=True)
class JobPolicy:

    tick_interval: float = 0.05

    max_concurrent_jobs: int = 32

    auto_restart_failed_jobs: bool = False