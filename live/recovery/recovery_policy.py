from dataclasses import dataclass


@dataclass(slots=True)
class RecoveryPolicy:

    max_attempts: int = 5

    retry_delay: float = 2.0

    exponential_backoff: bool = True

    backoff_multiplier: float = 2.0