from dataclasses import dataclass


@dataclass(slots=True)
class ExecutionConfig:

    retry_attempts: int = 5

    retry_delay: float = 2.0

    timeout: float = 15.0

    paper_mode: bool = False

    live_mode: bool = True

    validate_orders: bool = True

    enable_metrics: bool = True