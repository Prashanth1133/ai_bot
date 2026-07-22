from dataclasses import dataclass

import numpy as np


@dataclass(slots=True)
class DatasetSample:

    sequence: np.ndarray

    direction: int

    confidence: float

    tp: float

    sl: float

    regime: int

    timestamp: int

    symbol: str

    timeframe: str