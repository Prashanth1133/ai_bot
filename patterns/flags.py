from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(slots=True)
class FlagPattern:

    detected: bool

    bullish: bool

    confidence: float

    breakout_level: float


class FlagDetector:

    def detect(

        self,

        high,

        low,

        close,

    ) -> FlagPattern:

        high = np.asarray(high)

        low = np.asarray(low)

        close = np.asarray(close)

        if len(close) < 30:

            return FlagPattern(
                False,
                False,
                0.0,
                0.0,
            )

        impulse = close[-15] - close[-30]

        consolidation = np.std(close[-15:])

        bullish = impulse > 0

        confidence = min(

            abs(impulse) /

            (consolidation + 1e-6),

            1.0,

        )

        return FlagPattern(

            detected=confidence > 0.55,

            bullish=bullish,

            confidence=float(confidence),

            breakout_level=float(high[-1]),

        )