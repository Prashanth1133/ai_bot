
from __future__ import annotations

from features.registry import Feature


class FeatureEngine:
    """
    Central feature manager.

    Responsible for updating and retrieving
    features used by the AI pipeline.
    """

    def __init__(self, store):
        self.store = store

    # =====================================================
    # Order Flow
    # =====================================================

    def update_orderflow(
        self,
        symbol,
        metrics,
    ):
        self.store.update(
            symbol,
            Feature.CVD,
            metrics.cvd,
        )

        self.store.update(
            symbol,
            Feature.DELTA,
            metrics.delta,
        )

        self.store.update(
            symbol,
            Feature.BUY_VOLUME,
            metrics.buy_volume,
        )

        self.store.update(
            symbol,
            Feature.SELL_VOLUME,
            metrics.sell_volume,
        )

    # =====================================================
    # Generic Updates
    # =====================================================

    def update(
        self,
        symbol,
        feature,
        value,
    ):
        self.store.update(
            symbol,
            feature,
            value,
        )

    # =====================================================
    # Accessors
    # =====================================================

    def get(
        self,
        symbol,
        feature,
    ):
        return self.store.get(
            symbol,
            feature,
        )

    def get_all(
        self,
        symbol,
    ):
        return self.store.get_all(
            symbol,
        )

    # =====================================================
    # Utility
    # =====================================================

    def clear(
        self,
        symbol,
    ):
        self.store.clear(
            symbol,
        )

