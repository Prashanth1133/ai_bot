
from dataclasses import dataclass
from typing import Dict


@dataclass
class MultiTimeframeFeatures:
    """
    Features aggregated across multiple timeframes.
    """

    timeframe_scores: Dict[str, float]

    htf_trend: str = "UNKNOWN"

    alignment_score: float = 0.0


class MultiTimeframeFusion:
    """
    Combines multiple timeframe signals into a single score.
    """

    def fuse(
        self,
        features: MultiTimeframeFeatures,
    ) -> float:
        """
        Compute a simple alignment score.

        Example:
            1m  -> 0.7
            5m  -> 0.8
            15m -> 0.9
            1h  -> 0.6
        """

        if not features.timeframe_scores:
            return 0.0

        scores = list(
            features.timeframe_scores.values()
        )

        return sum(scores) / len(scores)

