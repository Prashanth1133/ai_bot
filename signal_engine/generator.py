from __future__ import annotations

from models.signal import Signal


class SignalGenerator:

    def generate(
        self,
        prediction,
    ) -> Signal:

        return Signal(
            symbol=prediction.symbol,
            action=prediction.action,
            confidence=prediction.confidence,
            score=prediction.confidence,
            strategy="AI",
            features={},
        )