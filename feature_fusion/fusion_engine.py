from __future__ import annotations

import numpy as np

from feature_fusion.feature_vector import FeatureVector
from feature_fusion.normalizer import FeatureNormalizer
from feature_fusion.schema import (
    UNIFIED_FEATURE_SCHEMA,
    NUM_UNIFIED_FEATURES,
)
from smart_money.break_of_structure import BOS
from smart_money.choch import CHOCH


class FeatureFusionEngine:

    def __init__(self):
        self.normalizer = FeatureNormalizer()

    @staticmethod
    def _float(value, default=0.0):
        try:
            if value is None:
                return float(default)

            value = float(value)

            if not np.isfinite(value):
                return float(default)

            return value

        except Exception:
            return float(default)

    @staticmethod
    def _direction(value):
        mapping = {
            "BULLISH": 1.0,
            "bullish": 1.0,
            "BUY": 1.0,
            "buy": 1.0,
            "BEARISH": -1.0,
            "bearish": -1.0,
            "SELL": -1.0,
            "sell": -1.0,
            "NEUTRAL": 0.0,
            "neutral": 0.0,
            "NONE": 0.0,
            "none": 0.0,
        }
        return mapping.get(str(value), 0.0)

    def build_from_snapshot(self, snapshot):
        mtf = snapshot.market.get("mtf", {})
        tf_data = mtf.get("timeframes", {})

        sr = snapshot.indicators.get(
            "support_resistance",
            {}
        )

        vp = snapshot.indicators.get(
            "volume_profile",
            {}
        )

        smc = snapshot.smart_money or {}
        patterns = snapshot.market.get(
            "patterns",
            {}
        )

        flow = snapshot.orderflow or {}
        news = snapshot.news or {}
        derivs = snapshot.derivatives or {}
        regime = snapshot.regime or {}
        onchain = snapshot.onchain or {}

        # -----------------------------------------------------
        # BASE PRICE
        # -----------------------------------------------------
        close_price = self._float(
            tf_data.get("5m", {}).get("close"),
            0.0,
        )

        if close_price <= 0:
            close_price = self._float(
                tf_data.get("1m", {}).get("close"),
                0.0,
            )

        # -----------------------------------------------------
        # DISTANCE
        # -----------------------------------------------------
        def distance_pct(target):
            target = self._float(target)
            if close_price <= 0 or target <= 0:
                return 0.0
            return (target - close_price) / close_price

        # -----------------------------------------------------
        # VOLUME
        # -----------------------------------------------------
        volume_5m = self._float(
            tf_data.get("5m", {}).get("volume"),
            0.0,
        )

        if volume_5m <= 0:
            volume_5m = self._float(
                tf_data.get("1m", {}).get("volume"),
                0.0,
            )

        # -----------------------------------------------------
        # FEATURE MAP
        # -----------------------------------------------------
        feature_map = {
            # MARKET
            "close_price": close_price,
            "returns_5m": self._float(
                tf_data.get("5m", {}).get("return"),
                tf_data.get("5m", {}).get("returns", 0.0),
            ),
            "volume_5m": volume_5m,
            "volatility_20m": self._float(
                tf_data.get("5m", {}).get("volatility"),
                0.0,
            ),

            # MTF
            "mtf_alignment_score": self._float(
                mtf.get("alignment_score"),
                0.0,
            ),
            "tf_1m_trend_score": self._float(
                tf_data.get("1m", {}).get("trend_score"),
                0.0,
            ),
            "tf_5m_trend_score": self._float(
                tf_data.get("5m", {}).get("trend_score"),
                0.0,
            ),
            "tf_15m_trend_score": self._float(
                tf_data.get("15m", {}).get("trend_score"),
                0.0,
            ),
            "tf_1h_trend_score": self._float(
                tf_data.get("1h", {}).get("trend_score"),
                0.0,
            ),
            "tf_4h_trend_score": self._float(
                tf_data.get("4h", {}).get("trend_score"),
                0.0,
            ),
            "tf_5m_rsi": self._float(
                tf_data.get("5m", {}).get("rsi"),
                50.0,
            ),
            "tf_15m_rsi": self._float(
                tf_data.get("15m", {}).get("rsi"),
                50.0,
            ),
            "tf_1h_rsi": self._float(
                tf_data.get("1h", {}).get("rsi"),
                50.0,
            ),

            # SR
            "support_distance_pct": self._float(
                sr.get("support_distance_pct"),
                0.0,
            ),
            "resistance_distance_pct": self._float(
                sr.get("resistance_distance_pct"),
                0.0,
            ),
            "support_strength": self._float(
                sr.get("support_strength"),
                0.0,
            ),
            "resistance_strength": self._float(
                sr.get("resistance_strength"),
                0.0,
            ),
            "touch_count_support": self._float(
                sr.get("touch_count_support"),
                0.0,
            ),
            "touch_count_resistance": self._float(
                sr.get("touch_count_resistance"),
                0.0,
            ),
            "breakout_flag": 1.0 if sr.get("breakout_status", False) else 0.0,
            "breakdown_flag": 1.0 if sr.get("breakdown_status", False) else 0.0,

            # SMC
            "smc_atr": self._float(
                smc.get("atr"),
                0.0,
            ),
            "smc_bos_flag": (
                0.0
                if smc.get("bos", BOS.NONE) in (BOS.NONE, None, 0, False, "NONE", "none")
                else 1.0
            ),
            "smc_choch_flag": (
                0.0
                if smc.get("choch", CHOCH.NONE) in (CHOCH.NONE, None, 0, False, "NONE", "none")
                else 1.0
            ),
            "smc_active_order_blocks": self._float(
                smc.get("active_order_blocks"),
                0.0,
            ),
            "smc_active_liquidity_zones": self._float(
                smc.get("active_liquidity_zones"),
                0.0,
            ),
            "smc_active_fvgs": self._float(
                smc.get("active_fvgs"),
                0.0,
            ),

            # PATTERNS
            "pattern_count": self._float(
                patterns.get("count"),
                0.0,
            ),
            "primary_pattern_direction": self._direction(
                patterns.get("primary_direction", "NEUTRAL")
            ),
            "primary_pattern_strength": self._float(
                patterns.get("primary_strength"),
                0.0,
            ),

            # ORDER FLOW
            "orderflow_cvd": self._float(
                flow.get("cvd"),
                0.0,
            ),
            "orderflow_delta": self._float(
                flow.get("delta"),
                0.0,
            ),
            "orderflow_buy_volume": self._float(
                flow.get("buy_volume"),
                0.0,
            ),
            "orderflow_sell_volume": self._float(
                flow.get("sell_volume"),
                0.0,
            ),
            "orderbook_imbalance": self._float(
                flow.get("imbalance"),
                0.0,
            ),

            # VOLUME PROFILE
            "vp_poc_distance_pct": distance_pct(vp.get("poc")),
            "vp_vah_distance_pct": distance_pct(vp.get("vah")),
            "vp_val_distance_pct": distance_pct(vp.get("val")),
            "vwap_distance_pct": distance_pct(vp.get("vwap")),

            # REGIME
            "regime_volatility": self._float(
                regime.get("volatility"),
                0.0,
            ),

            # DERIVATIVES
            "derivatives_funding_rate": self._float(
                derivs.get("funding_rate"),
                0.0,
            ),
            "derivatives_oi_change": self._float(
                derivs.get("open_interest_change"),
                0.0,
            ),
            "derivatives_taker_imbalance": self._float(
                derivs.get("taker_imbalance"),
                0.0,
            ),

            # NEWS
            "news_sentiment": self._float(
                news.get("sentiment"),
                0.0,
            ),
            "news_impact_score": self._float(
                news.get("impact_score"),
                0.0,
            ),
            "news_btc_relevance": self._float(
                news.get("btc_relevance"),
                0.0,
            ),

            # ONCHAIN
            "onchain_whale_score": self._float(
                onchain.get("whale_score"),
                0.0,
            ),
            "onchain_exchange_net_flow": self._float(
                onchain.get("exchange_net_flow"),
                0.0,
            ),
        }

        # -----------------------------------------------------
        # HARD 48-FEATURE CHECK
        # -----------------------------------------------------
        missing = [
            name
            for name in UNIFIED_FEATURE_SCHEMA
            if name not in feature_map
        ]

        if missing:
            raise RuntimeError(f"Missing unified features: {missing}")

        vector = np.asarray(
            [feature_map[name] for name in UNIFIED_FEATURE_SCHEMA],
            dtype=np.float32,
        )

        if vector.shape != (NUM_UNIFIED_FEATURES,):
            raise RuntimeError(
                f"Expected {NUM_UNIFIED_FEATURES} features, got {vector.shape}"
            )

        if not np.isfinite(vector).all():
            bad = [
                UNIFIED_FEATURE_SCHEMA[i]
                for i, x in enumerate(vector)
                if not np.isfinite(x)
            ]
            raise RuntimeError(f"Non-finite features: {bad}")

        return vector

    def build(
        self,
        symbol,
        timeframe,
        timestamp,
        modules,
    ):
        fv = FeatureVector(
            symbol,
            timeframe,
            timestamp,
        )

        for module in modules:
            if module is None:
                continue

            if isinstance(module, dict):
                for k, v in module.items():
                    fv.add(k, v)
            elif hasattr(module, "__dict__"):
                for k, v in vars(module).items():
                    fv.add(k, v)

        return self.normalizer.normalize(fv.get())