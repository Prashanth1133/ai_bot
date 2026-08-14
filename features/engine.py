
from decimal import Decimal

from features.registry import Feature


class FeatureEngine:
    """
    Central feature manager.

    Responsible for updating and retrieving
    features used by the AI pipeline.
    """

    def __init__(self, store=None):
        self.store = store

    # =====================================================
    # Order Flow
    # =====================================================

    def update_orderflow(
        self,
        symbol,
        metrics,
    ):
        if self.store is None:
            return

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
    # Order Book
    # =====================================================

    def update_orderbook(
        self,
        symbol,
        orderbook,
    ):
        if self.store is None or orderbook is None:
            return

        bid_volume = sum((level.quantity for level in orderbook.bids), Decimal("0"))
        ask_volume = sum((level.quantity for level in orderbook.asks), Decimal("0"))
        total_volume = bid_volume + ask_volume

        imbalance = (
            float((bid_volume - ask_volume) / total_volume)
            if total_volume > 0
            else 0.0
        )

        best_bid = orderbook.bids[0].price if orderbook.bids else None
        best_ask = orderbook.asks[0].price if orderbook.asks else None

        spread = (
            float(best_ask - best_bid)
            if (best_bid is not None and best_ask is not None)
            else 0.0
        )

        mid_price = (
            float((best_bid + best_ask) / Decimal("2"))
            if (best_bid is not None and best_ask is not None)
            else 0.0
        )

        self.store.update(symbol, Feature.BID_VOLUME, float(bid_volume))
        self.store.update(symbol, Feature.ASK_VOLUME, float(ask_volume))
        self.store.update(symbol, Feature.IMBALANCE, imbalance)
        self.store.update(symbol, Feature.SPREAD, spread)
        self.store.update(symbol, Feature.MID_PRICE, mid_price)

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

