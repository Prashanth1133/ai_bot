import numpy as np
import pickle
from dataset.labels import LabelConfig, DirectionLabel, RegimeLabel
from dataset.label_engine import LabelEngine
from market.historical import BinanceHistoricalData

def test():
    historical = BinanceHistoricalData()
    candles = historical.fetch_klines("BTCUSDT", "1m", 20000)
    closes = np.array([float(c.close) for c in candles], dtype=np.float64)
    highs = np.array([float(c.high) for c in candles], dtype=np.float64)
    lows = np.array([float(c.low) for c in candles], dtype=np.float64)

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

    print("Testing new reversal parameters and various regime settings...")
    cfg = LabelConfig(
        reversal_min_prior_move_atr=1.0,
        reversal_min_future_move_atr=1.0,
        reversal_min_directional_ratio=0.50,
        reversal_min_efficiency=0.15,
        reversal_retrace_fraction=0.35,
        reversal_min_bars=15,
    )
    engine = LabelEngine(cfg)
    
    reversals = []
    r240s = []
    atrs_pct = []
    for i in range(128, n - 240):
        entry = closes[i]
        atr_pct = atr[i] / entry
        r240 = (closes[i + 240] - entry) / entry
        res = engine.generate(closes, highs, lows, i, atr[i])
        if res is not None:
            reversals.append(res.reversal)
            r240s.append(r240)
            atrs_pct.append(atr_pct)
    
    r240s = np.array(r240s)
    atrs_pct = np.array(atrs_pct)
    rev_pct = 100.0 * np.sum(np.array(reversals) > 0.5) / len(reversals)
    print(f"New Reversal Rate: {rev_pct:.2f}% (Count: {int(np.sum(np.array(reversals) > 0.5))}/{len(reversals)})")

    print("\nRegime distributions with different atr multipliers:")
    for reg_mult in [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 8.0, 10.0]:
        reg_thresh = atrs_pct * reg_mult
        bull_pct = 100.0 * np.sum(r240s >= reg_thresh) / len(r240s)
        bear_pct = 100.0 * np.sum(r240s <= -reg_thresh) / len(r240s)
        range_pct = 100.0 * np.sum((r240s > -reg_thresh) & (r240s < reg_thresh)) / len(r240s)
        print(f"Multiplier: {reg_mult:4.1f}x ATR | BEAR: {bear_pct:5.2f}% | RANGE: {range_pct:5.2f}% | BULL: {bull_pct:5.2f}%")

    print("\nRegime distributions with fixed percentage thresholds:")
    for fixed_pct in [0.001, 0.002, 0.003, 0.004, 0.005]:
        bull_pct = 100.0 * np.sum(r240s >= fixed_pct) / len(r240s)
        bear_pct = 100.0 * np.sum(r240s <= -fixed_pct) / len(r240s)
        range_pct = 100.0 * np.sum((r240s > -fixed_pct) & (r240s < fixed_pct)) / len(r240s)
        print(f"Fixed Thresh: {fixed_pct*100:4.2f}% | BEAR: {bear_pct:5.2f}% | RANGE: {range_pct:5.2f}% | BULL: {bull_pct:5.2f}%")

if __name__ == "__main__":
    test()
