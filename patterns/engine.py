from __future__ import annotations

from patterns.single import SinglePatternDetector
from patterns.double import DoublePatternDetector
from patterns.triple import TriplePatternDetector


class PatternEngine:

    def __init__(self):
        self.single = SinglePatternDetector()
        self.double = DoublePatternDetector()
        self.triple = TriplePatternDetector()

    def detect(
        self,
        candles,
    ):
        if not candles:
            return []

        candles = sorted(
            candles,
            key=lambda c: int(getattr(c, "open_time", 0)),
        )
        results = []
        results.extend(self.single.detect(candles))
        results.extend(self.double.detect(candles))
        results.extend(self.triple.detect(candles))

        current_ts = getattr(candles[-1], "open_time", None)
        causal = []

        for pattern in results:
            ts = getattr(
                pattern,
                "open_time",
                getattr(pattern, "timestamp", None),
            )
            if ts is None or current_ts is None or ts <= current_ts:
                causal.append(pattern)

        return causal