from dataclasses import dataclass


@dataclass(slots=True)
class TrainingTarget:

    direction: int

    confidence: float

    tp: float

    sl: float

    regime: int