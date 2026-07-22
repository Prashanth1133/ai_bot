from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class LiveConfig:

    exchange: str = "BINANCE"

    environment: str = "LIVE"

    reconnect_interval: float = 5.0

    heartbeat_interval: float = 30.0

    scheduler_interval: float = 0.1

    recovery_enabled: bool = True

    monitoring_enabled: bool = True

    logging_enabled: bool = True

    metrics_enabled: bool = True

    services: dict = field(default_factory=dict)