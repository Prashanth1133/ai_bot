from dataclasses import dataclass


@dataclass(slots=True)
class SessionPolicy:

    reconnect: bool = True

    max_retries: int = 10

    retry_interval: float = 5.0

    heartbeat_timeout: float = 30.0