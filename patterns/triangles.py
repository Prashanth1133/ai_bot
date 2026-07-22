from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(slots=True)
class TrianglePattern:

    detected: bool

    type: str

    confidence: float

    breakout_price: float


class TriangleDetector:

    def detect(

        self,

        high,

        low,

    ):

        high = np.asarray(high)

        low = np.asarray(low)

        if len(high) < 30:

            return TrianglePattern(
                False,
                "NONE",
                0.0,
                0.0,
            )

        upper = np.polyfit(

            np.arange(20),

            high[-20:],

            1,

        )[0]

        lower = np.polyfit(

            np.arange(20),

            low[-20:],

            1,

        )[0]

        if upper < 0 and lower > 0:

            t = "SYMMETRICAL"

        elif upper < 0:

            t = "DESCENDING"

        elif lower > 0:

            t = "ASCENDING"

        else:

            t = "NONE"

        confidence = min(

            abs(upper - lower) * 50,

            1.0,

        )

        return TrianglePattern(

            t != "NONE",

            t,

            confidence,

            float(high[-1]),

        )