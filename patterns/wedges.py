from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(slots=True)
class WedgePattern:

    detected: bool

    type: str

    confidence: float


class WedgeDetector:

    def detect(

        self,

        high,

        low,

    ):

        high = np.asarray(high)

        low = np.asarray(low)

        if len(high) < 30:

            return WedgePattern(

                False,

                "NONE",

                0.0,

            )

        hs = np.polyfit(

            np.arange(20),

            high[-20:],

            1,

        )[0]

        ls = np.polyfit(

            np.arange(20),

            low[-20:],

            1,

        )[0]

        if hs > 0 and ls > 0:

            t = "RISING"

        elif hs < 0 and ls < 0:

            t = "FALLING"

        else:

            t = "NONE"

        confidence = min(

            abs(hs - ls) * 40,

            1.0,

        )

        return WedgePattern(

            t != "NONE",

            t,

            confidence,

        )