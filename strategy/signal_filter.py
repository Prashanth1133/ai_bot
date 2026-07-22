from __future__ import annotations


class SignalFilter:

    def __init__(
        self,
        confidence_threshold: float = 0.60,
    ):
        self.threshold = confidence_threshold

    def allow(
        self,
        result,
    ):

        if result is None:
            return False

        if result.signal == "HOLD":
            return False

        return result.confidence >= self.threshold