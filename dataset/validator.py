from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import numpy as np

from feature_fusion.schema import (
    UNIFIED_FEATURE_SCHEMA,
    NUM_UNIFIED_FEATURES,
)

FEATURE_RANGES = {
    "mtf_alignment_score": (0.0, 1.0),
    "tf_1m_trend_score": (-1.0, 1.0),
    "tf_5m_trend_score": (-1.0, 1.0),
    "tf_15m_trend_score": (-1.0, 1.0),
    "tf_1h_trend_score": (-1.0, 1.0),
    "tf_4h_trend_score": (-1.0, 1.0),
    "tf_5m_rsi": (0.0, 100.0),
    "tf_15m_rsi": (0.0, 100.0),
    "tf_1h_rsi": (0.0, 100.0),
    "support_strength": (0.0, 1.0),
    "resistance_strength": (0.0, 1.0),
    "breakout_flag": (0.0, 1.0),
    "breakdown_flag": (0.0, 1.0),
    "smc_bos_flag": (0.0, 1.0),
    "smc_choch_flag": (0.0, 1.0),
    "smc_active_order_blocks": (0.0, np.inf),
    "smc_active_liquidity_zones": (0.0, np.inf),
    "smc_active_fvgs": (0.0, np.inf),
    "orderbook_imbalance": (-1.0, 1.0),
    "derivatives_funding_rate": (-1.0, 1.0),
    "derivatives_taker_imbalance": (-1.0, 1.0),
    "news_sentiment": (-1.0, 1.0),
    "news_impact_score": (0.0, 1.0),
    "news_btc_relevance": (0.0, 1.0),
    "onchain_whale_score": (0.0, 1.0),
}


class DatasetValidator:
    """
    Causal Dataset Validator for the 48-feature schema.
    Verifies:
      - No NaN
      - No Inf
      - No constant features (std > 1e-8)
      - Correct shapes & dimensions ([N, 128, 48] or [N, 48])
      - Correct ranges for bounded technical / intelligence metrics
      - Monotonically increasing timestamps (no chronological leakage)
    """

    @staticmethod
    def validate(
        features,
        labels=None,
        timestamps=None,
        require_dynamic: bool = True,
        validate_ranges: bool = True,
    ) -> bool:
        features = np.asarray(features, dtype=np.float32)

        # -----------------------------------------------------
        # BASIC CHECKS
        # -----------------------------------------------------
        if features.size == 0:
            raise ValueError("Empty feature dataset")

        if labels is not None:
            labels = np.asarray(labels)
            if labels.size == 0:
                raise ValueError("Empty labels")
            if len(features) != len(labels):
                raise ValueError(
                    f"Feature/label sample mismatch: features={len(features)}, labels={len(labels)}"
                )
            if not np.isfinite(labels.astype(np.float64)).all():
                raise ValueError("Labels contain NaN/Inf")

        # -----------------------------------------------------
        # DIMENSIONS
        # -----------------------------------------------------
        if features.ndim not in (2, 3):
            raise ValueError(
                f"Expected 2D [N, {NUM_UNIFIED_FEATURES}] or 3D [N, SEQ, {NUM_UNIFIED_FEATURES}] features, "
                f"got {features.ndim}D shape={features.shape}"
            )

        if features.shape[-1] != NUM_UNIFIED_FEATURES:
            raise ValueError(
                f"Expected {NUM_UNIFIED_FEATURES} features, got {features.shape[-1]}"
            )

        # -----------------------------------------------------
        # FINITE (NO NaN / NO INF)
        # -----------------------------------------------------
        if not np.isfinite(features).all():
            raise ValueError("Features contain NaN or Inf values")

        # -----------------------------------------------------
        # FEATURE VARIANCE (NO CONSTANTS)
        # -----------------------------------------------------
        flat = features.reshape(-1, NUM_UNIFIED_FEATURES)
        constant = []

        for i, name in enumerate(UNIFIED_FEATURE_SCHEMA):
            std = float(np.std(flat[:, i]))
            if std <= 1e-8:
                constant.append(f"{name} (std={std:.10f})")

        if require_dynamic and constant:
            raise ValueError(
                "Constant features detected:\n" + "\n".join(f"  - {x}" for x in constant)
            )

        # -----------------------------------------------------
        # RANGE VALIDATION
        # -----------------------------------------------------
        if validate_ranges:
            for idx, name in enumerate(UNIFIED_FEATURE_SCHEMA):
                if name not in FEATURE_RANGES:
                    continue
                low, high = FEATURE_RANGES[name]
                col = flat[:, idx]
                col_min = float(np.min(col))
                col_max = float(np.max(col))
                if col_min < low - 1e-6 or col_max > high + 1e-6:
                    raise ValueError(
                        f"Feature range failure for '{name}': allowed=[{low}, {high}], actual=[{col_min}, {col_max}]"
                    )

        # -----------------------------------------------------
        # TIMESTAMPS (CHRONOLOGICAL ORDERING)
        # -----------------------------------------------------
        if timestamps is not None:
            ts = np.asarray(timestamps, dtype=np.int64)
            if len(ts) != len(features):
                raise ValueError(
                    f"Timestamp count mismatch: timestamps={len(ts)}, features={len(features)}"
                )
            if not np.all(np.diff(ts) > 0):
                raise ValueError("Timestamps are not strictly monotonically increasing")

        return True