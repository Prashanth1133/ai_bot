from dataclasses import dataclass


@dataclass(slots=True)
class TrainingConfig:

    epochs: int = 50

    batch_size: int = 64

    learning_rate: float = 1e-4

    weight_decay: float = 1e-4

    warmup_epochs: int = 3

    gradient_clip: float = 1.0

    early_stopping_patience: int = 10

    workers: int = 8

    device = "cuda"

    mixed_precision = True