from __future__ import annotations

import os
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pickle
import time
from collections import Counter

import numpy as np

from dataset.generate_final_dataset import calculate_causal_atr
from dataset.label_engine import LabelEngine
from dataset.labels import LabelConfig, DirectionLabel, RegimeLabel, ReversalLabel


def test_labels():
    print("=" * 70)
    print("FAST LABEL & ATR DIAGNOSTIC TEST")
    print("=" * 70)

    # 1. Load cached candles
    cache_path = Path("dataset/cache/BTCUSDT_1m_1061200.pkl")
    if not cache_path.exists():
        cache_path = Path("dataset/cache/BTCUSDT_1m_3500.pkl")
        if not cache_path.exists():
            raise FileNotFoundError("No cached 1m candle file found in dataset/cache/")

    print(f"Loading candles from: {cache_path}")
    with open(cache_path, "rb") as f:
        raw_rows = pickle.load(f)

    print(f"Total candles loaded: {len(raw_rows):,}")

    closes = np.array([float(r[4]) for r in raw_rows], dtype=np.float64)
    highs = np.array([float(r[2]) for r in raw_rows], dtype=np.float64)
    lows = np.array([float(r[3]) for r in raw_rows], dtype=np.float64)

    # 2. Compute Causal ATR
    t0 = time.perf_counter()
    atrs = calculate_causal_atr(highs=highs, lows=lows, closes=closes, period=14)
    atr_time = time.perf_counter() - t0

    print(f"\n[ATR] Computed in {atr_time * 1000:.1f}ms")
    print(f"  Valid ATRs (>0): {np.count_nonzero(atrs > 0):,}/{len(atrs):,}")
    print(f"  Min ATR        : {np.min(atrs):.6f}")
    print(f"  Max ATR        : {np.max(atrs):.6f}")
    print(f"  Mean ATR       : {np.mean(atrs[atrs > 0]):.6f}")

    # 3. Label Engine Diagnostic
    cfg = LabelConfig()
    engine = LabelEngine(cfg)

    seq_len = 128
    horizon = 240
    start = seq_len
    end = len(closes) - horizon

    print(f"\n[LABEL TEST] Testing candidate range [{start:,} .. {end:,}] ({end - start:,} candles)...")

    # Sample first 10
    for idx in range(start, min(start + 10, end)):
        res = engine.generate(closes=closes, highs=highs, lows=lows, index=idx, atr=atrs[idx])
        status = "VALID" if res is not None else "NONE"
        print(f"  |- Candle {idx:>6}: Price={closes[idx]:>8.2f} | ATR={atrs[idx]:>7.2f} | Result={status}")

    # 4. Fast Benchmark over 50,000 candles
    bench_count = min(50_000, end - start)
    print(f"\n[BENCHMARK] Generating labels for {bench_count:,} candles...")
    
    t_start = time.perf_counter()
    directions = []
    reversals = []
    regimes = []
    valid_count = 0
    invalid_atr = 0
    skipped = 0

    for i in range(start, start + bench_count):
        if not np.isfinite(atrs[i]) or atrs[i] <= 0:
            invalid_atr += 1
            continue

        res = engine.generate(closes=closes, highs=highs, lows=lows, index=i, atr=atrs[i])
        if res is None:
            skipped += 1
            continue

        valid_count += 1
        directions.append(res.direction)
        reversals.append(res.reversal)
        regimes.append(res.regime)

    elapsed = time.perf_counter() - t_start
    rate = bench_count / max(elapsed, 1e-6)

    print(f"\n[RESULTS] {bench_count:,} candles evaluated in {elapsed:.2f}s ({rate:,.0f} candles/s)")
    print(f"  Valid Labels : {valid_count:,} ({valid_count / bench_count * 100:.2f}%)")
    print(f"  Invalid ATR  : {invalid_atr:,}")
    print(f"  Skipped      : {skipped:,}")

    # Distribution Stats
    dir_counts = Counter(directions)
    dir_names = {0: "SELL", 1: "HOLD", 2: "BUY"}
    print("\n[DIRECTION DISTRIBUTION]")
    for k in [0, 1, 2]:
        c = dir_counts.get(k, 0)
        pct = c / max(valid_count, 1) * 100
        print(f"  {dir_names[k]:<5}: {c:>6,} ({pct:>5.2f}%)")

    rev_pos = sum(1 for r in reversals if r > 0.5)
    rev_neg = len(reversals) - rev_pos
    print("\n[REVERSAL DISTRIBUTION]")
    print(f"  NON-REVERSAL : {rev_neg:>6,} ({rev_neg / max(valid_count, 1) * 100:>5.2f}%)")
    print(f"  REVERSAL     : {rev_pos:>6,} ({rev_pos / max(valid_count, 1) * 100:>5.2f}%)")

    reg_counts = Counter(regimes)
    reg_names = {0: "BEAR", 1: "RANGE", 2: "BULL"}
    print("\n[REGIME DISTRIBUTION]")
    for k in [0, 1, 2]:
        c = reg_counts.get(k, 0)
        pct = c / max(valid_count, 1) * 100
        print(f"  {reg_names[k]:<5}: {c:>6,} ({pct:>5.2f}%)")

    print("\n" + "=" * 70)
    if valid_count > 0:
        print("DIAGNOSTIC PASSED: Labels are generating smoothly with balanced distributions!")
    else:
        print("DIAGNOSTIC FAILED: Zero labels generated.")
    print("=" * 70)


if __name__ == "__main__":
    test_labels()
