from __future__ import annotations

import asyncio
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

# Ensure project root is in sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import numpy as np
import torch

from market.historical import BinanceHistoricalData
from market.candle_manager import CandleManager

from features.orderflow import OrderFlowEngine, OrderFlowMetrics
from features.engine import FeatureEngine
from features.feature_store import FeatureStore

from context.context_builder import ContextBuilder
from context.context_registry import ContextRegistry

from context.context_providers import (
    MTFContextProvider,
    SRContextProvider,
    PatternContextProvider,
    SMCContextProvider,
    VolumeProfileContextProvider,
    MarketRegimeContextProvider,
)

from multi_timeframe.multi_timeframe_manager import MultiTimeframeManager
from indicators.support_resistance import SupportResistanceEngine
from patterns.engine import PatternEngine
from smart_money.engine import SmartMoneyEngine
from volume_profile.engine import VolumeProfileEngine
from market_regime.engine import MarketRegimeEngine

from feature_fusion.fusion_engine import FeatureFusionEngine
from feature_fusion.normalizer import FeatureNormalizer
from feature_fusion.schema import (
    NUM_UNIFIED_FEATURES,
    UNIFIED_FEATURE_SCHEMA,
    UNIFIED_FEATURE_NAMES,
)
from smart_money.break_of_structure import BOS
from smart_money.choch import CHOCH

from dataset.historical_intelligence import HistoricalIntelligence
from dataset.labels import DirectionLabel, RegimeLabel, ReversalLabel
from dataset.splitter import DatasetSplitter
from dataset.validator import DatasetValidator


# ============================================================
# CONFIGURATION
# ============================================================

SYMBOL = "BTCUSDT"
BASE_TIMEFRAME = "1m"
TIMEFRAMES = ["1m", "5m", "15m", "1h", "4h"]
SEQUENCE_LENGTH = 128
MAX_PREDICTION_HORIZON = 240
TWO_YEARS_1M = 1_051_200
HISTORY_BUFFER = 10_000

OUTPUT_PATH = "dataset/final_unified_dataset_v7.pt"
FEATURE_CHECKPOINT_VERSION = "FEATURES-48-V7"

RANGES = {
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


def calculate_causal_atr(
    highs: np.ndarray,
    lows: np.ndarray,
    closes: np.ndarray,
    period: int = 14,
) -> np.ndarray:
    highs = np.asarray(highs, dtype=np.float64)
    lows = np.asarray(lows, dtype=np.float64)
    closes = np.asarray(closes, dtype=np.float64)
    n = len(closes)
    atr = np.zeros(n, dtype=np.float64)

    if n == 0:
        return atr

    tr = np.zeros(n, dtype=np.float64)
    tr[0] = highs[0] - lows[0]

    for i in range(1, n):
        tr[i] = max(
            highs[i] - lows[i],
            abs(highs[i] - closes[i - 1]),
            abs(lows[i] - closes[i - 1]),
        )

    for i in range(period - 1, n):
        window = tr[i - period + 1 : i + 1]
        atr[i] = np.mean(window)

    return atr


def compute_structural_reversal(
    close_prices: np.ndarray | list[float],
    atr_pct: float,
    current_index: int,
    lookback_minutes: int = 60,
    future_horizon_minutes: int = 60,
    min_prior_move_atr: float = 1.0,
    min_future_move_atr: float = 0.75,
    min_directional_ratio: float = 0.55,
    retrace_fraction: float = 0.30,
    min_bars: int = 20,
) -> float:

    prices = np.asarray(
        close_prices,
        dtype=np.float64,
    )

    n = len(prices)

    if n == 0:
        return 0.0

    if current_index < lookback_minutes:
        return 0.0

    if current_index + future_horizon_minutes >= n:
        return 0.0

    if not np.isfinite(atr_pct) or atr_pct <= 0:
        return 0.0

    prior_start = current_index - lookback_minutes
    prior_end = current_index

    future_start = current_index
    future_end = current_index + future_horizon_minutes

    prior = prices[
        prior_start:prior_end + 1
    ]

    future = prices[
        future_start:future_end + 1
    ]

    if len(prior) < min_bars:
        return 0.0

    if len(future) < min_bars:
        return 0.0

    if not np.all(np.isfinite(prior)):
        return 0.0

    if not np.all(np.isfinite(future)):
        return 0.0

    prior_move = prior[-1] - prior[0]

    prior_return = (
        prior[-1] / prior[0]
    ) - 1.0

    prior_threshold = (
        min_prior_move_atr * atr_pct
    )

    # ---------------------------------------------------------
    # PRIOR TREND
    # ---------------------------------------------------------

    if prior_return >= prior_threshold:
        prior_direction = 1

    elif prior_return <= -prior_threshold:
        prior_direction = -1

    else:
        return 0.0

    prior_changes = np.diff(prior)

    if prior_direction > 0:
        prior_ratio = float(
            np.mean(prior_changes > 0)
        )
    else:
        prior_ratio = float(
            np.mean(prior_changes < 0)
        )

    if prior_ratio < min_directional_ratio:
        return 0.0

    # ---------------------------------------------------------
    # FUTURE OPPOSITE EXCURSION
    # ---------------------------------------------------------

    future_return = (
        future[-1] / future[0]
    ) - 1.0

    future_changes = np.diff(future)

    # Bullish prior -> bearish reversal
    if prior_direction > 0:

        future_extreme = float(
            np.min(future)
        )

        opposite_move = (
            future_extreme - future[0]
        ) / future[0]

        if opposite_move > -(
            min_future_move_atr * atr_pct
        ):
            return 0.0

        retracement = (
            prior[-1] - future_extreme
        )

        required_retrace = (
            abs(prior_move) * retrace_fraction
        )

        if retracement < required_retrace:
            return 0.0

    # Bearish prior -> bullish reversal
    else:

        future_extreme = float(
            np.max(future)
        )

        opposite_move = (
            future_extreme - future[0]
        ) / future[0]

        if opposite_move < (
            min_future_move_atr * atr_pct
        ):
            return 0.0

        retracement = (
            future_extreme - prior[-1]
        )

        required_retrace = (
            abs(prior_move) * retrace_fraction
        )

        if retracement < required_retrace:
            return 0.0

    # ---------------------------------------------------------
    # FUTURE DIRECTIONAL CONFIRMATION
    # ---------------------------------------------------------

    if prior_direction > 0:

        future_ratio = float(
            np.mean(future_changes < 0)
        )

    else:

        future_ratio = float(
            np.mean(future_changes > 0)
        )

    if future_ratio < 0.50:
        return 0.0

    return 1.0


def make_direction_label(
    future_returns_1h,
    future_returns_4h,
    threshold: float = 0.0015,
) -> int:
    """
    Causal multi-horizon direction target.

    Uses the actual future path from 1h and 4h.
    BUY/SELL thresholds are symmetric.

    The threshold is scaled by future-path dispersion so that
    high-volatility periods do not collapse into HOLD while
    low-volatility periods are not over-labeled as BUY/SELL.
    """

    future_returns_1h = np.asarray(future_returns_1h, dtype=np.float64)
    future_returns_4h = np.asarray(future_returns_4h, dtype=np.float64)

    if len(future_returns_1h) == 0 or len(future_returns_4h) == 0:
        return int(DirectionLabel.HOLD)

    r1 = float(np.mean(future_returns_1h))
    r4 = float(np.mean(future_returns_4h))

    combined = 0.65 * r1 + 0.35 * r4

    # Future-path volatility.
    vol_1h = float(np.std(future_returns_1h))
    vol_4h = float(np.std(future_returns_4h))

    path_volatility = 0.65 * vol_1h + 0.35 * vol_4h

    # Adaptive threshold.
    #
    # Keeps the original 0.15% threshold as the minimum,
    # but adapts to the actual volatility of the future path.
    adaptive_threshold = max(
        threshold,
        path_volatility * 0.50,
    )

    if combined >= adaptive_threshold:
        return int(DirectionLabel.BUY)

    if combined <= -adaptive_threshold:
        return int(DirectionLabel.SELL)

    return int(DirectionLabel.HOLD)


def validate_feature_matrix(
    feature_matrix: np.ndarray,
    feature_names: list[str],
    min_std: float = 1e-8,
) -> bool:
    X = np.asarray(feature_matrix, dtype=np.float64)

    if X.ndim != 2:
        raise RuntimeError(f"Feature matrix must be 2D, got shape={X.shape}")

    if X.shape[1] != len(feature_names):
        raise RuntimeError(
            f"Feature count mismatch: matrix={X.shape[1]} names={len(feature_names)}"
        )

    failures = []

    for i, name in enumerate(feature_names):
        values = X[:, i]
        finite = np.isfinite(values)
        finite_values = values[finite]

        if len(finite_values) == 0:
            failures.append((name, "NO_FINITE_VALUES"))
            continue

        std = float(np.std(finite_values))
        if std <= min_std:
            failures.append((name, f"CONSTANT (std={std:.10f})"))

        if not np.all(finite):
            failures.append((name, "NAN_OR_INF"))

    if failures:
        lines = [f"  - {name}: {reason}" for name, reason in failures]
        raise RuntimeError("FEATURE VALIDATION FAILED:\n" + "\n".join(lines))

    # Range validation
    for idx, name in enumerate(feature_names):
        if name not in RANGES:
            continue
        low, high = RANGES[name]
        column = X[:, idx]
        if np.any(column < low) or np.any(column > high):
            raise RuntimeError(
                f"FEATURE RANGE FAILURE: {name} range=[{low}, {high}] "
                f"actual=[{np.nanmin(column)}, {np.nanmax(column)}]"
            )

    return True


# ============================================================
# DATASET GENERATOR
# ============================================================

async def generate_dataset(
    symbol: str = SYMBOL,
    output_path: str = OUTPUT_PATH,
    days: int | None = 15,
):
    print("=" * 70)
    print("FINAL DATASET GENERATOR V6 (48 DYNAMIC FEATURES)")
    print("=" * 70)

    duration_str = f"{days} days" if days else "2 years (full)"
    print(f"Symbol        : {symbol}")
    print(f"Duration      : {duration_str}")
    print(f"Base TF       : {BASE_TIMEFRAME}")
    print(f"MTF           : {TIMEFRAMES}")
    print(f"Sequence      : {SEQUENCE_LENGTH}")
    print(f"Features      : {NUM_UNIFIED_FEATURES}")
    print(f"Output        : {output_path}")
    print("=" * 70)

    # 1. Historical 1m Data
    print("\n[1/7] Loading 1m historical data...")
    historical = BinanceHistoricalData()

    if days is not None:
        needed_1m = (days * 24 * 60) + SEQUENCE_LENGTH + MAX_PREDICTION_HORIZON + 5000
    else:
        needed_1m = TWO_YEARS_1M + HISTORY_BUFFER

    candles_1m = await asyncio.to_thread(
        historical.fetch_klines,
        symbol,
        BASE_TIMEFRAME,
        needed_1m,
        True,
    )

    candles_1m = sorted(
        candles_1m,
        key=lambda c: getattr(c, "open_time", 0),
    )

    if not candles_1m or len(candles_1m) < (SEQUENCE_LENGTH + MAX_PREDICTION_HORIZON + 100):
        raise RuntimeError(f"Insufficient 1m candles: {len(candles_1m) if candles_1m else 0}")

    print(f"Loaded {len(candles_1m):,} 1m candles")
    first_1m_open_time = getattr(candles_1m[0], "open_time", 0)

    # 2. MTF History
    print("\n[2/7] Loading MTF history...")
    tf_candles_dict: dict[str, list] = {}

    for tf in TIMEFRAMES:
        if tf == "1m":
            tf_candles = candles_1m
        else:
            tf_multiplier = {"5m": 5, "15m": 15, "1h": 60, "4h": 240}[tf]
            limit_tf = max(5000, len(candles_1m) // tf_multiplier + 1000)
            raw_mtf = await asyncio.to_thread(
                historical.fetch_klines,
                symbol,
                tf,
                limit_tf,
                True,
            )

            raw_mtf = sorted(
                raw_mtf,
                key=lambda c: getattr(c, "open_time", 0),
            )

            last_1m_close_time = getattr(candles_1m[-1], "close_time", 0)

            tf_candles = [
                c
                for c in raw_mtf
                if first_1m_open_time
                <= getattr(c, "close_time", 0)
                <= last_1m_close_time
            ]
            if not tf_candles:
                tf_candles = raw_mtf[-min(len(raw_mtf), 1000) :]

        if not tf_candles:
            raise RuntimeError(f"No historical data for {tf}")

        tf_candles_dict[tf] = tf_candles
        print(f"{tf:<5} : {len(tf_candles):,} candles")

    # 3. Engines
    print("\n[3/7] Initializing feature engines...")
    candle_manager = CandleManager()
    mtf_manager = MultiTimeframeManager()
    sr_engine = SupportResistanceEngine()
    pattern_engine = PatternEngine()
    smc_engine = SmartMoneyEngine()
    vp_engine = VolumeProfileEngine()
    regime_engine = MarketRegimeEngine()
    fusion_engine = FeatureFusionEngine()

    # Context Registry
    registry = ContextRegistry()
    registry.register("mtf", MTFContextProvider(mtf_manager))
    registry.register("sr", SRContextProvider(sr_engine, candle_manager))
    registry.register("patterns", PatternContextProvider(pattern_engine, candle_manager))
    registry.register("smc", SMCContextProvider(smc_engine, candle_manager))
    registry.register("volume_profile", VolumeProfileContextProvider(vp_engine, candle_manager))
    registry.register("regime", MarketRegimeContextProvider(regime_engine))

    builder = ContextBuilder(registry)

    # Historical Intelligence Alignment Layer
    historical_intelligence = HistoricalIntelligence(
        candles=candles_1m,
    )

    # 4. Causal Feature Generation
    print("\n[4/7] Building causal feature matrix with 48 dynamic features...")
    n = len(candles_1m)

    closes = np.array([float(c.close) for c in candles_1m], dtype=np.float64)
    highs = np.array([float(c.high) for c in candles_1m], dtype=np.float64)
    lows = np.array([float(c.low) for c in candles_1m], dtype=np.float64)

    atrs = calculate_causal_atr(highs=highs, lows=lows, closes=closes, period=14)
    feature_matrix = np.zeros((n, NUM_UNIFIED_FEATURES), dtype=np.float32)

    mtf_pointers = {tf: 0 for tf in ["5m", "15m", "1h", "4h"]}
    stage_start = time.perf_counter()
    LOG_INTERVAL = 10_000

    for i in range(n):
        candle = candles_1m[i]
        candle_manager.update(candle)
        mtf_manager.update_candle(candle)

        curr_close_time = getattr(candle, "close_time", 0)

        # Causally stream HTF closed candles up to current 1m close time.
        #
        # IMPORTANT:
        # CandleManager is the BASE_TIMEFRAME (1m) history used by
        # SR / Pattern / SMC / Volume Profile providers.
        # HTF candles must NOT be inserted into CandleManager.
        # MultiTimeframeManager owns the HTF streams separately.
        for tf in ["5m", "15m", "1h", "4h"]:
            htf_candles = tf_candles_dict.get(tf, [])
            ptr = mtf_pointers[tf]

            while ptr < len(htf_candles) and getattr(
                htf_candles[ptr], "close_time", 0
            ) <= curr_close_time:
                mtf_manager.update_candle(htf_candles[ptr])
                ptr += 1

            mtf_pointers[tf] = ptr

        # Build core technical context snapshot
        snapshot = builder.build(symbol, BASE_TIMEFRAME)

        # Inject historical intelligence (order flow from taker volume, derivatives, news, on-chain)
        intel = historical_intelligence.get(candle)

        snapshot.orderflow = {
            "cvd": intel.orderflow_cvd,
            "delta": intel.orderflow_delta,
            "buy_volume": intel.orderflow_buy_volume,
            "sell_volume": intel.orderflow_sell_volume,
            "imbalance": intel.orderbook_imbalance,
        }

        snapshot.derivatives = {
            "funding_rate": intel.derivatives_funding_rate,
            "open_interest_change": intel.derivatives_oi_change,
            "taker_imbalance": intel.derivatives_taker_imbalance,
        }

        snapshot.news = {
            "sentiment": intel.news_sentiment,
            "impact_score": intel.news_impact_score,
            "btc_relevance": intel.news_btc_relevance,
        }

        snapshot.onchain = {
            "whale_score": intel.onchain_whale_score,
            "exchange_net_flow": intel.onchain_exchange_net_flow,
        }

        vector = fusion_engine.build_from_snapshot(snapshot)
        feature_matrix[i] = vector

        # Relationship checks (correlate flags with underlying engine events)
        smc_dict = snapshot.smart_money or {}
        bos_val = smc_dict.get("bos", BOS.NONE)
        choch_val = smc_dict.get("choch", CHOCH.NONE)
        sr_dict = snapshot.indicators.get("support_resistance", {})

        bos_flag_val = vector[UNIFIED_FEATURE_SCHEMA.index("smc_bos_flag")]
        choch_flag_val = vector[UNIFIED_FEATURE_SCHEMA.index("smc_choch_flag")]
        breakout_flag_val = vector[UNIFIED_FEATURE_SCHEMA.index("breakout_flag")]
        breakdown_flag_val = vector[UNIFIED_FEATURE_SCHEMA.index("breakdown_flag")]

        if bos_flag_val > 0.5 and (bos_val == BOS.NONE or bos_val is None):
            raise RuntimeError("[SEMANTIC FAIL] BOS flag/enumeration mismatch")
        if choch_flag_val > 0.5 and (choch_val == CHOCH.NONE or choch_val is None):
            raise RuntimeError("[SEMANTIC FAIL] CHoCH flag/enumeration mismatch")
        if breakout_flag_val > 0.5 and not sr_dict.get("breakout_status", False):
            raise RuntimeError("[SEMANTIC FAIL] Breakout without resistance crossing")
        if breakdown_flag_val > 0.5 and not sr_dict.get("breakdown_status", False):
            raise RuntimeError("[SEMANTIC FAIL] Breakdown without support crossing")

        if i == 0 or i % 1000 == 0 or i == n - 1:
            elapsed = time.perf_counter() - stage_start
            rate = i / elapsed if elapsed > 0 and i > 0 else 0.0
            remaining = (n - i) / rate if rate > 0 else 0.0
            print(
                f"[FEATURES] {i:,}/{n:,} ({i / n * 100:6.2f}%) rate={rate:,.1f}/s ETA={remaining / 60:.1f}m",
                flush=True,
            )

    # 48 Feature Integrity & Range Validation
    print()
    print("=" * 70)
    print("48 FEATURE INTEGRITY")
    print("=" * 70)

    for i, name in enumerate(UNIFIED_FEATURE_SCHEMA):
        col = feature_matrix[:, i]
        std = float(np.std(col))
        minimum = float(np.min(col))
        maximum = float(np.max(col))
        mean = float(np.mean(col))

        print(
            f"{i:02d} {name:<35} "
            f"min={minimum:>12.6f} max={maximum:>12.6f} "
            f"mean={mean:>12.6f} std={std:>12.6f}"
        )

    print("=" * 70)

    # Strict Validation against constant / NaN / Inf / Range failures
    validate_feature_matrix(feature_matrix, UNIFIED_FEATURE_SCHEMA, min_std=1e-8)
    print("\n48/48 FEATURES DYNAMIC & IN RANGE: PASS")

    # Event Feature Semantic Diagnostics & Validation
    EVENT_FEATURES = [
        "breakout_flag",
        "breakdown_flag",
        "smc_bos_flag",
        "smc_choch_flag",
    ]
    STRENGTH_FEATURES = [
        "support_strength",
        "resistance_strength",
    ]
    TOUCH_FEATURES = [
        "touch_count_support",
        "touch_count_resistance",
    ]

    EVENT_MAX_ACTIVE_RATIO = 0.20
    MIN_STRENGTH_STD = 0.02
    MAX_TOUCH_MEAN = 20.0

    print()
    print("=" * 70)
    print("EVENT & S/R FEATURE SEMANTIC DIAGNOSTICS")
    print("=" * 70)

    for name in EVENT_FEATURES:
        if name in UNIFIED_FEATURE_SCHEMA:
            idx = UNIFIED_FEATURE_SCHEMA.index(name)
            col = feature_matrix[:, idx]
            active_ratio = float((col > 0.5).mean())
            active_count = int((col > 0.5).sum())
            status = "PASS (SPARSE EVENT)" if active_ratio <= EVENT_MAX_ACTIVE_RATIO else "FAIL (SATURATED)"
            print(
                f"{name:<30s} active={active_ratio * 100:7.3f}% | count={active_count:>8,} | {status}"
            )
            if active_ratio > EVENT_MAX_ACTIVE_RATIO:
                raise RuntimeError(
                    f"[SEMANTIC FAIL] {name} active ratio {active_ratio:.2%} > 20%. Expected sparse event behavior."
                )

    print()
    for name in STRENGTH_FEATURES:
        if name in UNIFIED_FEATURE_SCHEMA:
            idx = UNIFIED_FEATURE_SCHEMA.index(name)
            col = feature_matrix[:, idx]
            mean = float(np.mean(col))
            std = float(np.std(col))
            p05 = float(np.percentile(col, 5))
            p50 = float(np.percentile(col, 50))
            p95 = float(np.percentile(col, 95))
            status = "PASS" if std >= MIN_STRENGTH_STD else "FAIL"
            print(
                f"{name:<30s} mean={mean:.4f} std={std:.4f} | p05={p05:.4f} p50={p50:.4f} p95={p95:.4f} | {status}"
            )
            if std < MIN_STRENGTH_STD:
                raise RuntimeError(
                    f"[SEMANTIC FAIL] {name} has insufficient variation (std={std:.6f} < 0.02)"
                )

    print()
    for name in TOUCH_FEATURES:
        if name in UNIFIED_FEATURE_SCHEMA:
            idx = UNIFIED_FEATURE_SCHEMA.index(name)
            col = feature_matrix[:, idx]
            mean = float(np.mean(col))
            max_v = float(np.max(col))
            p50 = float(np.percentile(col, 50))
            p95 = float(np.percentile(col, 95))
            status = "PASS" if mean <= MAX_TOUCH_MEAN else "FAIL"
            print(
                f"{name:<30s} mean={mean:.3f} max={max_v:.1f} | median={p50:.1f} p95={p95:.1f} | {status}"
            )
            if mean > MAX_TOUCH_MEAN:
                raise RuntimeError(
                    f"[SEMANTIC FAIL] {name} still appears unclustered (mean={mean:.2f} > 20.0)"
                )

    print("=" * 70)
    print("FEATURE SEMANTICS: ALL CHECKS PASSED (Events < 20%, S/R Distributed, Touches Clustered)")

    # 5. Multi-Horizon Future-Path Target Generation
    print("\n[5/7] Generating future-path targets (15m, 30m, 1h, 4h)...")

    sequences = []
    directions = []
    reversals = []
    regimes = []

    returns_15m = []
    returns_30m = []
    returns_1h = []
    returns_4h = []

    max_returns_15m = []
    min_returns_15m = []
    max_returns_1h = []
    min_returns_1h = []
    max_returns_4h = []
    min_returns_4h = []

    take_profits = []
    stop_losses = []
    future_highs = []
    future_lows = []
    timestamps = []

    start_idx = SEQUENCE_LENGTH
    end_idx = n - MAX_PREDICTION_HORIZON
    total_candidates = end_idx - start_idx
    label_start = time.perf_counter()

    for i in range(start_idx, end_idx):
        entry_price = float(closes[i])
        if entry_price <= 0:
            continue

        atr_val = atrs[i]
        if atr_val <= 0 or not np.isfinite(atr_val):
            continue
        atr_pct = atr_val / entry_price

        # Future returns series
        fut_ret_15m_arr = (closes[i + 1 : i + 16] / entry_price) - 1.0
        fut_ret_30m_arr = (closes[i + 1 : i + 31] / entry_price) - 1.0
        fut_ret_1h_arr = (closes[i + 1 : i + 61] / entry_price) - 1.0
        fut_ret_4h_arr = (closes[i + 1 : i + 241] / entry_price) - 1.0

        if len(fut_ret_4h_arr) < 240:
            continue

        # Point returns
        r15 = (closes[i + 15] - entry_price) / entry_price
        r30 = (closes[i + 30] - entry_price) / entry_price
        r60 = (closes[i + 60] - entry_price) / entry_price
        r240 = (closes[i + 240] - entry_price) / entry_price

        # Future high / low slices
        slice_15_high = (highs[i + 1 : i + 16] - entry_price) / entry_price
        slice_15_low = (lows[i + 1 : i + 16] - entry_price) / entry_price

        slice_1h_high = (highs[i + 1 : i + 61] - entry_price) / entry_price
        slice_1h_low = (lows[i + 1 : i + 61] - entry_price) / entry_price

        slice_4h_high = (highs[i + 1 : i + 241] - entry_price) / entry_price
        slice_4h_low = (lows[i + 1 : i + 241] - entry_price) / entry_price

        max_r15 = float(np.max(slice_15_high))
        min_r15 = float(np.min(slice_15_low))

        max_r1h = float(np.max(slice_1h_high))
        min_r1h = float(np.min(slice_1h_low))

        max_r4h = float(np.max(slice_4h_high))
        min_r4h = float(np.min(slice_4h_low))

        # Direction from path
        direction_label = make_direction_label(fut_ret_1h_arr, fut_ret_4h_arr)

        # Reversal from structural path
        reversal_label = compute_structural_reversal(
            close_prices=closes,
            atr_pct=atr_pct,
            current_index=i,
            lookback_minutes=60,
            future_horizon_minutes=60,
            min_prior_move_atr=1.0,
            min_future_move_atr=0.75,
            min_directional_ratio=0.55,
            retrace_fraction=0.30,
            min_bars=20,
        )

        # Regime from 4h return and ATR
        regime_thresh = max(0.005, atr_pct * 3.0)
        if r240 >= regime_thresh:
            regime_label = int(RegimeLabel.BULL)
        elif r240 <= -regime_thresh:
            regime_label = int(RegimeLabel.BEAR)
        else:
            regime_label = int(RegimeLabel.RANGE)

        # Dynamic TP / SL targets based only on information available
        # at the prediction point.
        #
        # Future excursion remains stored separately as:
        # max_future_return_* / min_future_return_*
        #
        # TP/SL are therefore executable ATR-relative targets rather
        # than future-information-derived targets.
        tp = float(np.clip(atr_pct * 2.0, 0.002, 0.08))
        sl = float(np.clip(atr_pct * 1.0, 0.001, 0.04))

        # Sequence slice [128, 48]
        seq = feature_matrix[i - SEQUENCE_LENGTH : i]
        if not np.isfinite(seq).all():
            continue

        sequences.append(seq)
        directions.append(direction_label)
        reversals.append(reversal_label)
        regimes.append(regime_label)

        returns_15m.append(r15)
        returns_30m.append(r30)
        returns_1h.append(r60)
        returns_4h.append(r240)

        max_returns_15m.append(max_r15)
        min_returns_15m.append(min_r15)
        max_returns_1h.append(max_r1h)
        min_returns_1h.append(min_r1h)
        max_returns_4h.append(max_r4h)
        min_returns_4h.append(min_r4h)

        take_profits.append(tp)
        stop_losses.append(sl)
        future_highs.append(float(np.max(highs[i + 1 : i + 61])))
        future_lows.append(float(np.min(lows[i + 1 : i + 61])))

        ts = getattr(candles_1m[i], "close_time", getattr(candles_1m[i], "open_time", i))
        timestamps.append(int(ts))

        if len(sequences) % 50000 == 0 or i == end_idx - 1:
            lbl_elapsed = time.perf_counter() - label_start
            lbl_rate = (i - start_idx + 1) / max(lbl_elapsed, 1e-6)
            print(
                f"  |- [TARGETS] {i - start_idx + 1:>10,}/{total_candidates:,} | "
                f"Valid: {len(sequences):,} | Rate: {lbl_rate:>7.1f} samples/s",
                flush=True,
            )

    n_samples = len(sequences)
    print(f"\n[TARGETS] Valid sample count: {n_samples:,}")

    # Clip to duration if requested
    if days is not None:
        target_len = days * 24 * 60
        if len(sequences) > target_len:
            sequences = sequences[-target_len:]
            directions = directions[-target_len:]
            reversals = reversals[-target_len:]
            regimes = regimes[-target_len:]
            returns_15m = returns_15m[-target_len:]
            returns_30m = returns_30m[-target_len:]
            returns_1h = returns_1h[-target_len:]
            returns_4h = returns_4h[-target_len:]
            max_returns_15m = max_returns_15m[-target_len:]
            min_returns_15m = min_returns_15m[-target_len:]
            max_returns_1h = max_returns_1h[-target_len:]
            min_returns_1h = min_returns_1h[-target_len:]
            max_returns_4h = max_returns_4h[-target_len:]
            min_returns_4h = min_returns_4h[-target_len:]
            take_profits = take_profits[-target_len:]
            stop_losses = stop_losses[-target_len:]
            future_highs = future_highs[-target_len:]
            future_lows = future_lows[-target_len:]
            timestamps = timestamps[-target_len:]
            print(f"[DURATION] Clipped to requested {days} days ({len(sequences):,} samples)")

    # 6. Convert to Tensors
    sequences_tensor = torch.from_numpy(np.asarray(sequences, dtype=np.float32))
    labels_tensor = torch.from_numpy(np.asarray(directions, dtype=np.int64))
    reversals_tensor = torch.from_numpy(np.asarray(reversals, dtype=np.float32))
    regimes_tensor = torch.from_numpy(np.asarray(regimes, dtype=np.int64))

    future_return_15m_tensor = torch.from_numpy(np.asarray(returns_15m, dtype=np.float32))
    future_return_30m_tensor = torch.from_numpy(np.asarray(returns_30m, dtype=np.float32))
    future_return_1h_tensor = torch.from_numpy(np.asarray(returns_1h, dtype=np.float32))
    future_return_4h_tensor = torch.from_numpy(np.asarray(returns_4h, dtype=np.float32))

    max_future_return_15m_tensor = torch.from_numpy(np.asarray(max_returns_15m, dtype=np.float32))
    min_future_return_15m_tensor = torch.from_numpy(np.asarray(min_returns_15m, dtype=np.float32))
    max_future_return_1h_tensor = torch.from_numpy(np.asarray(max_returns_1h, dtype=np.float32))
    min_future_return_1h_tensor = torch.from_numpy(np.asarray(min_returns_1h, dtype=np.float32))
    max_future_return_4h_tensor = torch.from_numpy(np.asarray(max_returns_4h, dtype=np.float32))
    min_future_return_4h_tensor = torch.from_numpy(np.asarray(min_returns_4h, dtype=np.float32))

    take_profits_tensor = torch.from_numpy(np.asarray(take_profits, dtype=np.float32))
    stop_losses_tensor = torch.from_numpy(np.asarray(stop_losses, dtype=np.float32))
    future_high_tensor = torch.from_numpy(np.asarray(future_highs, dtype=np.float32))
    future_low_tensor = torch.from_numpy(np.asarray(future_lows, dtype=np.float32))
    timestamps_tensor = torch.from_numpy(np.asarray(timestamps, dtype=np.int64))

    # 7. Pre-Save Gate & Causal Validation
    sequence_length = SEQUENCE_LENGTH

    target_lengths = {
        "labels": len(labels_tensor),
        "reversals": len(reversals_tensor),
        "regimes": len(regimes_tensor),
        "return_15m": len(future_return_15m_tensor),
        "return_30m": len(future_return_30m_tensor),
        "return_1h": len(future_return_1h_tensor),
        "return_4h": len(future_return_4h_tensor),
        "max_return_15m": len(max_future_return_15m_tensor),
        "min_return_15m": len(min_future_return_15m_tensor),
        "max_return_1h": len(max_future_return_1h_tensor),
        "min_return_1h": len(min_future_return_1h_tensor),
        "max_return_4h": len(max_future_return_4h_tensor),
        "min_return_4h": len(min_future_return_4h_tensor),
        "take_profits": len(take_profits_tensor),
        "stop_losses": len(stop_losses_tensor),
        "future_high": len(future_high_tensor),
        "future_low": len(future_low_tensor),
        "timestamps": len(timestamps_tensor),
    }

    sequence_count = len(sequences_tensor)

    invalid_lengths = {
        name: length
        for name, length in target_lengths.items()
        if length != sequence_count
    }

    if invalid_lengths:
        raise RuntimeError(
            f"TARGET LENGTH MISMATCH: expected {sequence_count}, "
            f"got {invalid_lengths}"
        )

    assert torch.isfinite(sequences_tensor).all()
    assert torch.isfinite(labels_tensor.float()).all()
    assert torch.isfinite(reversals_tensor).all()

    # Full Causal Validation via DatasetValidator
    DatasetValidator.validate(
        features=sequences_tensor.numpy(),
        labels=labels_tensor.numpy(),
        timestamps=timestamps_tensor.numpy(),
        require_dynamic=True,
        validate_ranges=True,
    )

    # Label Distribution Check
    unique_labels = torch.unique(labels_tensor).tolist()
    if not set(unique_labels).issubset({0, 1, 2}):
        raise RuntimeError(f"Invalid direction labels: {unique_labels}")

    # Reversal Check
    unique_reversals = torch.unique(reversals_tensor).tolist()
    if not set(unique_reversals).issubset({0.0, 1.0}):
        raise RuntimeError("Invalid reversal target")

    print()
    print("=" * 70)
    print("FINAL PRE-SAVE GATE & CAUSAL VALIDATION")
    print("=" * 70)
    print("Samples   :", len(sequences_tensor))
    print("Sequence  :", sequences_tensor.shape[1])
    print("Features  :", sequences_tensor.shape[2])
    print("NaN Count :", torch.isnan(sequences_tensor).sum().item())
    print("Inf Count :", torch.isinf(sequences_tensor).sum().item())
    print("Dynamic   : 48/48 (std > 1e-8)")
    print("Ranges    : 48/48 Validated")
    print("Timestamps: Monotonically Increasing (Pass)")
    print(
        "Direction :",
        {
            int(k): int(v)
            for k, v in zip(*np.unique(labels_tensor.numpy(), return_counts=True))
        },
    )
    print("FINAL PRE-SAVE GATE: PASS")
    print("=" * 70)

    # 8. Chronological Purged Candle Split
    n_total = len(sequences_tensor)
    splitter = DatasetSplitter(
        sequence_length=SEQUENCE_LENGTH,
        max_horizon=MAX_PREDICTION_HORIZON,
    )
    split_indices = splitter.split_indices(
        total_samples=n_total,
        train_ratio=0.70,
        validation_ratio=0.15,
    )

    train_start, train_end = split_indices["train"]
    val_start, val_end = split_indices["validation"]
    test_start, test_end = split_indices["test"]
    purge_gap = splitter.purge_gap

    splits_meta = {
        "train": [train_start, train_end],
        "purge_1": [train_end, val_start],
        "validation": [val_start, val_end],
        "purge_2": [val_end, test_start],
        "test": [test_start, test_end],
        "purge_gap": purge_gap,
    }

    # 9. Pack Dataset Bundle
    dataset_dict = {
        "sequences": sequences_tensor,
        "labels": labels_tensor,
        "reversals": reversals_tensor,
        "regimes": regimes_tensor,
        "future_return_15m": future_return_15m_tensor,
        "future_return_30m": future_return_30m_tensor,
        "future_return_1h": future_return_1h_tensor,
        "future_return_4h": future_return_4h_tensor,
        "max_future_return_15m": max_future_return_15m_tensor,
        "min_future_return_15m": min_future_return_15m_tensor,
        "max_future_return_1h": max_future_return_1h_tensor,
        "min_future_return_1h": min_future_return_1h_tensor,
        "max_future_return_4h": max_future_return_4h_tensor,
        "min_future_return_4h": min_future_return_4h_tensor,
        "take_profits": take_profits_tensor,
        "stop_losses": stop_losses_tensor,
        "future_high": future_high_tensor,
        "future_low": future_low_tensor,
        "timestamps": timestamps_tensor,
        "feature_names": UNIFIED_FEATURE_SCHEMA,
        "feature_schema": UNIFIED_FEATURE_SCHEMA,
        "symbol": symbol,
        "base_timeframe": BASE_TIMEFRAME,
        "timeframes": TIMEFRAMES,
        "feature_dim": 48,
        "sequence_length": 128,
        "prediction_horizons": [15, 30, 60, 240],
        "dataset_version": "FINAL-1M-MTF-V7",
        "feature_version": "FEATURES-48-V7",
        "label_version": "LABELS-PATH-MULTI-HORIZON-V7",
        "splits": splits_meta,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }

    # 10. Pre-save integrity checks
    if not np.isfinite(feature_matrix).all():
        raise RuntimeError(
            "FINAL DATASET FAILED: NaN/Inf detected"
        )

    if feature_matrix.shape[1] != NUM_UNIFIED_FEATURES:
        raise RuntimeError(
            "FINAL DATASET FAILED: feature dimension mismatch"
        )

    for name in EVENT_FEATURES:
        if name not in UNIFIED_FEATURE_SCHEMA:
            continue
        idx = UNIFIED_FEATURE_SCHEMA.index(name)
        active_ratio = float(
            np.mean(
                feature_matrix[:, idx] > 0.5
            )
        )
        if active_ratio > 0.20:
            raise RuntimeError(
                f"FINAL DATASET FAILED: "
                f"{name} active ratio="
                f"{active_ratio:.2%}"
            )

    for name in STRENGTH_FEATURES:
        if name not in UNIFIED_FEATURE_SCHEMA:
            continue
        idx = UNIFIED_FEATURE_SCHEMA.index(name)
        std = float(
            np.std(
                feature_matrix[:, idx]
            )
        )
        if std < 0.02:
            raise RuntimeError(
                f"FINAL DATASET FAILED: "
                f"{name} std={std:.6f}"
            )

    # 11. Save
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    torch.save(dataset_dict, output_path)

    print(f"\n[SAVED] Final 48-feature dataset bundle saved successfully to: {output_path}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="CryptoVisionAI Final Dataset Generator V6")
    parser.add_argument(
        "--days",
        type=int,
        default=15,
        help="Number of days of 1m data to generate (default: 15)",
    )
    parser.add_argument(
        "--symbol",
        type=str,
        default=SYMBOL,
        help=f"Trading pair symbol (default: {SYMBOL})",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=OUTPUT_PATH,
        help=f"Output path for .pt dataset (default: {OUTPUT_PATH})",
    )

    args = parser.parse_args()
    days_val = args.days if args.days and args.days > 0 else None

    asyncio.run(
        generate_dataset(
            symbol=args.symbol,
            output_path=args.output,
            days=days_val,
        )
    )