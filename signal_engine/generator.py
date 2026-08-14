from __future__ import annotations

from models.signal import Signal


class SignalGenerator:

    def generate(
        self,
        prediction,
    ) -> Signal:

        if prediction is None:
            return None

        return Signal(

            symbol=prediction.symbol,

            action=prediction.action,

            confidence=float(
                prediction.confidence
            ),

            score=float(
                prediction.confidence
            ),

            strategy="AI",

            features=getattr(

                prediction,
                "features",
                {}

            ),

        )