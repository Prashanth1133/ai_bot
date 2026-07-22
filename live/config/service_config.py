from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class ServiceConfig:

    enabled: bool = True

    auto_restart: bool = True

    max_restart_attempts: int = 10

    startup_timeout: float = 30.0

    shutdown_timeout: float = 30.0