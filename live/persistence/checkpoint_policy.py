from dataclasses import dataclass


@dataclass(slots=True)
class CheckpointPolicy:

    interval_seconds: int = 300

    max_checkpoints: int = 100

    compress: bool = False

    auto_restore: bool = True