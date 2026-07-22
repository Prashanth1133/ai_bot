from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class RuntimeConfig:

    workers: int = 4

    event_queue_size: int = 10000

    execution_queue_size: int = 5000

    prediction_queue_size: int = 5000

    storage_queue_size: int = 5000

    max_memory_mb: int = 4096