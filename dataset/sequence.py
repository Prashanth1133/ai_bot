from dataclasses import dataclass

import numpy as np


@dataclass(slots=True)
class FeatureSequence:

    symbol: str

    timeframe: str

    timestamp: int

    features: np.ndarray

    label: int | None = None