from dataclasses import dataclass


@dataclass(slots=True)
class NotificationPolicy:

    enabled: bool = True

    minimum_level: str = "INFO"

    retry_attempts: int = 3

    timeout: float = 5.0