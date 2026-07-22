from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class PredictionResult:

    direction: str

    confidence: float

    probabilities: list[float]

    timestamp: int

    model_version: str