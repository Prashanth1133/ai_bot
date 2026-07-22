from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(slots=True)
class HarmonicPattern:

    detected: bool

    pattern: str

    confidence: float


class HarmonicDetector:

    PATTERNS = (

        "GARTLEY",

        "BAT",

        "CRAB",

        "BUTTERFLY",

    )

    def detect(

        self,

        swings,

    ):

        swings = np.asarray(

            swings,

            dtype=float,

        )

        if len(swings) < 5:

            return HarmonicPattern(

                False,

                "NONE",

                0.0,

            )

        xa = abs(swings[1] - swings[0])

        ab = abs(swings[2] - swings[1])

        ratio = ab / (xa + 1e-9)

        if 0.55 <= ratio <= 0.70:

            return HarmonicPattern(

                True,

                "GARTLEY",

                0.75,

            )

        if 0.35 <= ratio <= 0.55:

            return HarmonicPattern(

                True,

                "BAT",

                0.70,

            )

        return HarmonicPattern(

            False,

            "NONE",

            0.0,

        )