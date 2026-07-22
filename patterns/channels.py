from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(slots=True)
class ChannelPattern:

    detected: bool

    direction: str

    upper: float

    lower: float

    confidence: float


class ChannelDetector:

    def detect(

        self,

        high,

        low,

    ):

        high = np.asarray(high)

        low = np.asarray(low)

        if len(high) < 20:

            return ChannelPattern(
                False,
                "NONE",
                0,
                0,
                0,
            )

        upper = np.mean(high[-20:])

        lower = np.mean(low[-20:])

        slope = np.polyfit(

            np.arange(20),

            (high[-20:] + low[-20:]) / 2,

            1,

        )[0]

        if slope > 0:

            direction = "UP"

        elif slope < 0:

            direction = "DOWN"

        else:

            direction = "SIDEWAYS"

        return ChannelPattern(

            True,

            direction,

            float(upper),

            float(lower),

            min(abs(slope) * 20, 1.0),

        )