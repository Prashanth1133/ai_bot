from __future__ import annotations

from models.signal import Signal


class SignalValidator:

    MIN_CONFIDENCE = 0.60

    VALID_ACTIONS = {

        "BUY",
        "SELL",
        "HOLD",

    }

    def validate(
        self,
        signal: Signal,
    ) -> bool:

        if signal is None:
            return False

        if signal.action not in self.VALID_ACTIONS:
            return False

        if signal.confidence < self.MIN_CONFIDENCE:
            return False

        return True