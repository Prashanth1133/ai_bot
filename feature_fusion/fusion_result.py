from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np


@dataclass(slots=True)
class FusionResult:

    symbol: str

    vector: np.ndarray

    feature_names: list[str]

    metadata: dict = field(default_factory=dict)