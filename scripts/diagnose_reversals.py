from __future__ import annotations

import os
import sys
import pickle
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import numpy as np

from market.historical import BinanceHistoricalData
from dataset.generate_final_dataset import calculate_causal_atr
from dataset.label_engine import compute_structural_reversal


def run_reversal_sweep():
    print("=" * 75)
    print("STRUCTURAL REVERSAL THRESHOLD SWEEP ON REAL BTCUSDT (15-DAY 1M CACHE)")
    print("=" * 75)

    # 1. Load candles via BinanceHistoricalData (which uses the cache automatically)
    fetcher = BinanceHistoricalData()
    candles = fetcher.fetch_klines(symbol="BTCUSDT", interval="1m", limit=26968, use_cache=True)
    if not candles:
        raise RuntimeError("Could not load BTC 1m candles")

    closes = np.array([float(c.close) for c in candles], dtype=np.float64)
    highs = np.array([float(c.high) for c in candles], dtype=np.float64)
    lows = np.array([float(c.low) for c in candles], dtype=np.float64)

    n = len(closes)
    print(f"Total 1m candles: {n:,}")

    atrs = calculate_causal_atr(highs=highs, lows=lows, closes=closes, period=14)

    # Configurations to test
    configs = [
        {
            "name": "Very Strict (1.50 ATR / 1.50 ATR / 50% retrace)",
            "prior_atr": 1.50,
            "future_atr": 1.50,
            "dir_ratio": 0.55,
            "retrace": 0.50,
        },
        {
            "name": "Strict      (1.25 ATR / 1.00 ATR / 40% retrace)",
            "prior_atr": 1.25,
            "future_atr": 1.00,
            "dir_ratio": 0.55,
            "retrace": 0.40,
        },
        {
            "name": "Moderate    (1.00 ATR / 0.75 ATR / 30% retrace) [Recommended]",
            "prior_atr": 1.00,
            "future_atr": 0.75,
            "dir_ratio": 0.55,
            "retrace": 0.30,
        },
        {
            "name": "Balanced    (0.85 ATR / 0.60 ATR / 25% retrace)",
            "prior_atr": 0.85,
            "future_atr": 0.60,
            "dir_ratio": 0.50,
            "retrace": 0.25,
        },
        {
            "name": "Loose       (0.75 ATR / 0.50 ATR / 25% retrace)",
            "prior_atr": 0.75,
            "future_atr": 0.50,
            "dir_ratio": 0.50,
            "retrace": 0.25,
        },
    ]

    start_idx = 128
    end_idx = n - 240
    total_valid = end_idx - start_idx

    print(f"Evaluating candidate windows: {start_idx:,} .. {end_idx:,} (N = {total_valid:,})\n")
    print(f"{'Configuration':<52} | {'Positives':>9} | {'Reversal Rate':>13} | {'Status'}")
    print("-" * 90)

    for cfg in configs:
        positives = 0
        for i in range(start_idx, end_idx):
            entry_price = float(closes[i])
            if entry_price <= 0:
                continue
            atr_val = atrs[i]
            if atr_val <= 0 or not np.isfinite(atr_val):
                continue
            atr_pct = atr_val / entry_price

            rev = compute_structural_reversal(
                close_prices=closes,
                atr_pct=atr_pct,
                current_index=i,
                lookback_minutes=60,
                future_horizon_minutes=60,
                min_prior_move_atr=cfg["prior_atr"],
                min_future_move_atr=cfg["future_atr"],
                min_directional_ratio=cfg["dir_ratio"],
                retrace_fraction=cfg["retrace"],
                min_bars=20,
            )
            if rev > 0.5:
                positives += 1

        rate = (positives / total_valid) * 100.0
        if 5.0 <= rate <= 15.0:
            status = "IDEAL (5–15%)"
        elif rate < 5.0:
            status = "LOW (< 5%)"
        else:
            status = "HIGH (> 15%)"

        print(f"{cfg['name']:<52} | {positives:>9,} | {rate:12.2f}% | {status}")

    print("=" * 75)


if __name__ == "__main__":
    run_reversal_sweep()
