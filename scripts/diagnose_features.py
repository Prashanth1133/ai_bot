from __future__ import annotations

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from dataclasses import dataclass
from decimal import Decimal
import numpy as np

from smart_money.engine import SmartMoneyEngine
from indicators.support_resistance import SupportResistanceEngine
from feature_fusion.fusion_engine import FeatureFusionEngine
from feature_fusion.schema import UNIFIED_FEATURE_SCHEMA


@dataclass
class Candle:
    symbol: str
    interval: str
    open_time: int
    open: Decimal
    high: Decimal
    low: Decimal
    close: Decimal
    volume: Decimal
    close_time: int


def generate_synthetic_candles(n=1000, start_price=50000.0, wave=True):
    np.random.seed(42)
    candles = []
    price = start_price
    t0 = 1700000000000

    for i in range(n):
        if wave:
            import math
            price = start_price + 400.0 * math.sin(i / 15.0) + (i * 0.8) + np.random.normal(0, 5)
        else:
            delta = np.random.normal(0, 30)
            price = max(100.0, price + delta)
        close = price
        high = close + abs(np.random.normal(15, 5))
        low = close - abs(np.random.normal(15, 5))
        high = max(high, close + 5)
        low = min(low, close - 5)
        vol = max(1.0, np.random.normal(10, 3))
        candles.append(
            Candle(
                symbol="BTCUSDT",
                interval="1m",
                open_time=t0 + i * 60000,
                open=Decimal(str(round(price, 2))),
                high=Decimal(str(round(high, 2))),
                low=Decimal(str(round(low, 2))),
                close=Decimal(str(round(close, 2))),
                volume=Decimal(str(round(vol, 4))),
                close_time=t0 + (i + 1) * 60000 - 1,
            )
        )
    return candles


from market.historical import BinanceHistoricalData
from models.market import Candle as ModelCandle


def evaluate_candles(candles, title="DIAGNOSTIC"):
    smc_engine = SmartMoneyEngine()
    sr_engine = SupportResistanceEngine(window=5, tolerance_pct=0.003, max_lookback=200)

    bos_flags = []
    choch_flags = []
    breakout_flags = []
    breakdown_flags = []
    support_strengths = []
    resistance_strengths = []
    support_touches = []
    resistance_touches = []

    for i in range(30, len(candles)):
        window = candles[max(0, i - 200) : i + 1]
        smc_res = smc_engine.process(window)
        sr_res = sr_engine.analyze(window)

        class MockSnapshot:
            market = {"mtf": {"timeframes": {"1m": {"close": float(window[-1].close)}}}, "patterns": {}}
            indicators = {"support_resistance": sr_res, "volume_profile": {}}
            smart_money = smc_res
            orderflow = {}
            derivatives = {}
            news = {}
            onchain = {}
            regime = {}

        fusion = FeatureFusionEngine()
        vector = fusion.build_from_snapshot(MockSnapshot())

        bos_flags.append(vector[UNIFIED_FEATURE_SCHEMA.index("smc_bos_flag")])
        choch_flags.append(vector[UNIFIED_FEATURE_SCHEMA.index("smc_choch_flag")])
        breakout_flags.append(vector[UNIFIED_FEATURE_SCHEMA.index("breakout_flag")])
        breakdown_flags.append(vector[UNIFIED_FEATURE_SCHEMA.index("breakdown_flag")])
        support_strengths.append(vector[UNIFIED_FEATURE_SCHEMA.index("support_strength")])
        resistance_strengths.append(vector[UNIFIED_FEATURE_SCHEMA.index("resistance_strength")])
        support_touches.append(vector[UNIFIED_FEATURE_SCHEMA.index("touch_count_support")])
        resistance_touches.append(vector[UNIFIED_FEATURE_SCHEMA.index("touch_count_resistance")])

    print("=" * 70)
    print(f"{title} (N = {len(bos_flags)} steps)")
    print("=" * 70)

    bos_arr = np.asarray(bos_flags)
    choch_arr = np.asarray(choch_flags)
    bo_arr = np.asarray(breakout_flags)
    bd_arr = np.asarray(breakdown_flags)

    print(f"BOS active %         : {(bos_arr > 0.5).mean() * 100:6.2f}% (count: {int((bos_arr > 0.5).sum())}/{len(bos_arr)})")
    print(f"CHoCH active %       : {(choch_arr > 0.5).mean() * 100:6.2f}% (count: {int((choch_arr > 0.5).sum())}/{len(choch_arr)})")
    print(f"Breakout active %    : {(bo_arr > 0.5).mean() * 100:6.2f}% (count: {int((bo_arr > 0.5).sum())}/{len(bo_arr)})")
    print(f"Breakdown active %   : {(bd_arr > 0.5).mean() * 100:6.2f}% (count: {int((bd_arr > 0.5).sum())}/{len(bd_arr)})")

    def print_strength_block(name, vals):
        arr = np.asarray(vals)
        mean = float(np.mean(arr))
        std = float(np.std(arr))
        p05 = float(np.percentile(arr, 5))
        p50 = float(np.percentile(arr, 50))
        p95 = float(np.percentile(arr, 95))
        print(f"\n{name}")
        print(f"  mean : {mean:.4f}")
        print(f"  std  : {std:.4f}")
        print(f"  p05  : {p05:.4f}")
        print(f"  p50  : {p50:.4f}")
        print(f"  p95  : {p95:.4f}")

    def print_touch_block(name, vals):
        arr = np.asarray(vals)
        mean = float(np.mean(arr))
        median = float(np.percentile(arr, 50))
        p95 = float(np.percentile(arr, 95))
        max_v = float(np.max(arr))
        print(f"\n{name}")
        print(f"  mean   : {mean:.3f}")
        print(f"  median : {median:.1f}")
        print(f"  p95    : {p95:.1f}")
        print(f"  max    : {max_v:.1f}")

    print_strength_block("Support strength", support_strengths)
    print_strength_block("Resistance strength", resistance_strengths)
    print_touch_block("Support touches", support_touches)
    print_touch_block("Resistance touches", resistance_touches)
    print("=" * 70)


def run_diagnostics():
    # 1. Synthetic wave candles
    syn_candles = generate_synthetic_candles(1000, wave=True)
    evaluate_candles(syn_candles, title="SYNTHETIC WAVE DATA DIAGNOSTIC")

    # 2. Real BTCUSDT cached / historical candles
    try:
        fetcher = BinanceHistoricalData()
        real_candles = fetcher.fetch_klines(symbol="BTCUSDT", interval="1m", limit=1000)
        if real_candles and len(real_candles) >= 100:
            print()
            evaluate_candles(real_candles, title="REAL BTCUSDT SEMANTIC DIAGNOSTIC")
    except Exception as e:
        print(f"[NOTE] Real BTC data fetch skipped / offline: {e}")


if __name__ == "__main__":
    run_diagnostics()
