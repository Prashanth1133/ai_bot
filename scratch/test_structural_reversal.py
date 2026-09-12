import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import numpy as np
from dataset.label_engine import LabelEngine
from dataset.labels import LabelConfig, ReversalLabel


def main():

    print("=" * 70)
    print("STRUCTURAL REVERSAL LABEL TEST")
    print("=" * 70)

    # Synthetic bullish -> bearish reversal
    prices = np.array([
        100.0, 100.2, 100.4, 100.6, 100.8, 101.0,
        101.2, 101.4, 101.6, 101.8, 102.0,
        101.8, 101.6, 101.4, 101.2, 101.0,
        100.8, 100.6, 100.4, 100.2, 100.0,
    ])

    atr_pct = 0.002
    cfg = LabelConfig(
        reversal_lookback_minutes=10,
        reversal_future_horizon_minutes=10,
        reversal_min_prior_atr=1.0,
        reversal_min_future_atr=1.0,
        reversal_min_prior_consistency=0.55,
        reversal_min_future_consistency=0.55,
        reversal_min_retrace=0.50,
    )
    engine = LabelEngine(cfg)

    result = engine._detect_reversal(
        closes=prices,
        index=10,
        atr_pct=atr_pct,
    )

    print("Expected structural reversal: 1.0")
    print("Actual:", result)

    assert result == 1.0

    # Test continuous uptrend (bullish -> bullish = non-reversal 0.0)
    prices_uptrend = np.array([100.0 + 0.2 * i for i in range(21)])
    result_uptrend = engine._detect_reversal(
        closes=prices_uptrend,
        index=10,
        atr_pct=atr_pct,
    )
    print("Expected continuous uptrend: 0.0")
    print("Actual:", result_uptrend)
    assert result_uptrend == 0.0

    print()
    print("PASS: Structural reversal unit test succeeded!")


if __name__ == "__main__":
    main()
