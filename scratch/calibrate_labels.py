from __future__ import annotations

import sys
import numpy as np
from market.historical import BinanceHistoricalData
from dataset.labels import LabelConfig, DirectionLabel, RegimeLabel, ReversalLabel
from dataset.label_engine import LabelEngine


def main():
    print("=" * 70)
    print("SMALL REAL-DATA LABEL CALIBRATION (20,000 1m CANDLES)")
    print("=" * 70)

    historical = BinanceHistoricalData()
    print("Fetching 20,000 1m candles for BTCUSDT...")
    candles = historical.fetch_klines("BTCUSDT", "1m", 20000)
    print(f"Loaded {len(candles)} candles.")

    closes = np.array([float(c.close) for c in candles], dtype=np.float64)
    highs = np.array([float(c.high) for c in candles], dtype=np.float64)
    lows = np.array([float(c.low) for c in candles], dtype=np.float64)

    # Compute rolling 14 ATR
    n = len(candles)
    tr = np.zeros(n, dtype=np.float64)
    tr[0] = highs[0] - lows[0]
    tr[1:] = np.maximum(
        highs[1:] - lows[1:],
        np.maximum(
            np.abs(highs[1:] - closes[:-1]),
            np.abs(lows[1:] - closes[:-1]),
        ),
    )
    atr = np.zeros(n, dtype=np.float64)
    for i in range(n):
        s = max(0, i - 13)
        atr[i] = max(np.mean(tr[s : i + 1]), closes[i] * 0.0001)

    cfg = LabelConfig()
    engine = LabelEngine(cfg)

    results = []
    for i in range(128, n - 240):
        res = engine.generate(closes, highs, lows, i, atr[i])
        if res is not None:
            results.append(res)

    print(f"\nTotal Generated Samples: {len(results):,}")

    directions = np.array([r.direction for r in results])
    reversals = np.array([r.reversal for r in results])
    regimes = np.array([r.regime for r in results])
    tps = np.array([r.take_profit for r in results])
    sls = np.array([r.stop_loss for r in results])
    r15s = np.array([r.future_return_15m for r in results])
    r60s = np.array([r.future_return_1h for r in results])
    r240s = np.array([r.future_return_4h for r in results])

    total = len(results)

    print("\n" + "-" * 70)
    print("DIRECTION")
    print("-" * 70)
    for label, name in [(0, "SELL"), (1, "HOLD"), (2, "BUY")]:
        c = int(np.sum(directions == label))
        print(f"{name:<8}: {c:,} ({100.0 * c / total:.2f}%)")

    print("\n" + "-" * 70)
    print("REVERSAL")
    print("-" * 70)
    rev_cnt = int(np.sum(reversals > 0.5))
    no_rev_cnt = total - rev_cnt
    print(f"NO REVERSAL: {no_rev_cnt:,} ({100.0 * no_rev_cnt / total:.2f}%)")
    print(f"REVERSAL   : {rev_cnt:,} ({100.0 * rev_cnt / total:.2f}%)")

    print("\n" + "-" * 70)
    print("REGIME (4H)")
    print("-" * 70)
    for label, name in [(0, "BEAR"), (1, "RANGE"), (2, "BULL")]:
        c = int(np.sum(regimes == label))
        print(f"{name:<8}: {c:,} ({100.0 * c / total:.2f}%)")

    print("\n" + "-" * 70)
    print("TP / SL / RETURNS STATISTICS")
    print("-" * 70)
    print(f"TP  : min={tps.min():.6f}, max={tps.max():.6f}, std={tps.std():.6f}")
    print(f"SL  : min={sls.min():.6f}, max={sls.max():.6f}, std={sls.std():.6f}")
    print(f"R15 : min={r15s.min():.6f}, max={r15s.max():.6f}, std={r15s.std():.6f}")
    print(f"R60 : min={r60s.min():.6f}, max={r60s.max():.6f}, std={r60s.std():.6f}")
    print(f"R240: min={r240s.min():.6f}, max={r240s.max():.6f}, std={r240s.std():.6f}")

    assert tps.std() > 0, "TP std must be > 0"
    assert sls.std() > 0, "SL std must be > 0"
    assert 0.001 <= (rev_cnt / total) <= 0.40, f"Reversal rate {rev_cnt/total:.4f} outside expected range"

    print("\n" + "=" * 70)
    print("CALIBRATION AUDIT: PASSED")
    print("=" * 70)


if __name__ == "__main__":
    main()
