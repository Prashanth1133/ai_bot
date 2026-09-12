from __future__ import annotations

import gc
import os
import time
from datetime import datetime, timezone
import numpy as np
import torch

from dataset.schema import (
    UNIFIED_FEATURE_SCHEMA,
    NUM_UNIFIED_FEATURES,
    MTF_SUFFIXES,
)
from dataset.labels import LabelConfig
from dataset.label_engine import LabelEngine
from dataset.normalization import FeatureNormalizer
from dataset.splitter import DatasetSplitter
from dataset.leakage import LeakageChecker
from dataset.validator import DatasetValidator
from dataset.generate_final_dataset import (
    fetch_two_years_1m,
    verify_1m_history,
    aggregate_bars,
    build_features,
    build_targets,
    slice_targets,
    print_storage_estimate,
    HISTORY_DAYS,
    TARGET_1M_CANDLES,
    SEQUENCE_LENGTH,
    TRAIN_RATIO,
    VALIDATION_RATIO,
    TEST_RATIO,
    LABEL_HORIZON_MINUTES,
    EMBARGO,
    TIMEFRAMES,
    FEATURE_DTYPE,
)


SYMBOLS = [
    "BTCUSDT",
    "ETHUSDT",
    "DOGEUSDT",
]

DEFAULT_OUTPUT_PATH = "dataset/final_unified_dataset_v2.pt"


def generate_single_coin_data(symbol: str) -> dict:
    """
    Generate point-in-time features, targets, and chronological splits for a single symbol.
    """
    coin_start = time.perf_counter()
    print("\n" + "=" * 80)
    print(f" PROCESSING COIN: {symbol}")
    print("=" * 80)

    # 1. Historical 1m data
    print(f"\n[{symbol} 1/6] Downloading 2-year 1m historical data...")
    candles_1m = fetch_two_years_1m(symbol)
    verify_1m_history(candles_1m)

    # 2. MTF aggregation
    print(f"\n[{symbol} 2/6] Aggregating synchronized MTF bars...")
    mtf = {tf: aggregate_bars(candles_1m, tf) for tf in TIMEFRAMES}

    # 3. 400-dim feature matrix computation
    print(f"\n[{symbol} 3/6] Computing 400 point-in-time features...")
    features = build_features(mtf)

    # 4. Target generation (with structural reversal)
    print(f"\n[{symbol} 4/6] Computing targets with structural reversal...")
    targets = build_targets(candles_1m)
    sample_count = len(targets["direction"])

    # 5. Alignment & Validation
    print(f"\n[{symbol} 5/6] Aligning and validating...")
    feature_start = SEQUENCE_LENGTH
    feature_end = feature_start + sample_count
    features = features[feature_start:feature_end]

    if len(features) != sample_count:
        raise RuntimeError(f"Alignment failure for {symbol}: {len(features)} != {sample_count}")

    LeakageChecker.check_feature_matrix(features)
    LeakageChecker.check_labels(targets["direction"], sample_count)
    DatasetValidator.validate(features, targets["direction"])

    # 6. Chronological split with embargo
    print(f"\n[{symbol} 6/6] Splitting chronologically (70/15/15) with 240m embargo...")
    splitter = DatasetSplitter()
    splits = splitter.split(
        sample_count,
        train_ratio=TRAIN_RATIO,
        validation_ratio=VALIDATION_RATIO,
    )

    train_start, train_end = splits["train"]
    val_start, val_end = splits["validation"]
    test_start, test_end = splits["test"]

    orig_val_start, orig_test_start = val_start, test_start
    val_start += EMBARGO
    test_start += EMBARGO

    normalizer = FeatureNormalizer()
    train_features = normalizer.fit_transform(features[train_start:train_end])
    val_features = normalizer.transform(features[val_start:val_end])
    test_features = normalizer.transform(features[test_start:test_end])

    train_targets = slice_targets(targets, train_start, train_end)
    val_targets = slice_targets(targets, val_start, val_end)
    test_targets = slice_targets(targets, test_start, test_end)

    elapsed = time.perf_counter() - coin_start
    print(f"[{symbol}] Completed in {elapsed / 60.0:.2f} min. Train: {len(train_features):,}, Val: {len(val_features):,}, Test: {len(test_features):,}")

    del features, candles_1m, mtf
    gc.collect()

    return {
        "train": {
            "features": torch.from_numpy(np.asarray(train_features, dtype=np.float32)),
            **train_targets,
        },
        "validation": {
            "features": torch.from_numpy(np.asarray(val_features, dtype=np.float32)),
            **val_targets,
        },
        "test": {
            "features": torch.from_numpy(np.asarray(test_features, dtype=np.float32)),
            **test_targets,
        },
        "normalization": normalizer.state_dict(),
        "sample_count": sample_count,
        "train_samples": len(train_features),
        "validation_samples": len(val_features),
        "test_samples": len(test_features),
        "original_val_start": int(orig_val_start),
        "original_test_start": int(orig_test_start),
    }


def generate_multicoin_dataset(
    symbols: list[str] = SYMBOLS,
    output_path: str = DEFAULT_OUTPUT_PATH,
) -> str:
    total_start = time.perf_counter()

    print("\n" + "=" * 80)
    print(" GENERATING MULTI-COIN DATASET (BTCUSDT + ETHUSDT + DOGEUSDT)")
    print(f" Symbols: {symbols}")
    print(f" Output : {output_path}")
    print("=" * 80)

    coin_data = {}
    symbol_to_id = {sym: idx for idx, sym in enumerate(symbols)}

    for sym in symbols:
        coin_data[sym] = generate_single_coin_data(sym)

    # Assemble master multi-coin bundle
    bundle = {
        **{sym: {
            "train": coin_data[sym]["train"],
            "validation": coin_data[sym]["validation"],
            "test": coin_data[sym]["test"],
            "normalization": coin_data[sym]["normalization"],
        } for sym in symbols},

        # Top-level multi-coin metadata & schema
        "symbols": list(symbols),
        "symbol_to_id": symbol_to_id,
        "feature_names": list(UNIFIED_FEATURE_SCHEMA),
        "feature_dim": int(NUM_UNIFIED_FEATURES),
        "sequence_length": int(SEQUENCE_LENGTH),
        "prediction_horizon_minutes": int(LABEL_HORIZON_MINUTES),
        "base_timeframe": "1m",
        "timeframes": list(TIMEFRAMES),
        "label_version": "final_v2_structural_reversal",
        "dataset_version": "final_v2_multicoin_structural_reversal",
        "label_configuration": {
            "direction": "UNCHANGED_FROM_FINAL_V1",
            "return_15m": "UNCHANGED_FROM_FINAL_V1",
            "return_1h": "UNCHANGED_FROM_FINAL_V1",
            "return_4h": "UNCHANGED_FROM_FINAL_V1",
            "max_return_1h": "UNCHANGED_FROM_FINAL_V1",
            "min_return_1h": "UNCHANGED_FROM_FINAL_V1",
            "take_profit": "UNCHANGED_FROM_FINAL_V1",
            "stop_loss": "UNCHANGED_FROM_FINAL_V1",
            "reversal": {
                "method": "structural_trend_reversal",
                "lookback_minutes": 60,
                "future_horizon_minutes": 60,
                "min_prior_move_atr": 1.5,
                "min_future_move_atr": 1.5,
                "min_directional_ratio": 0.55,
                "min_bars": 30,
            },
        },
        "metadata": {
            "created_at": datetime.now(timezone.utc).isoformat(),
            "history_days": HISTORY_DAYS,
            "target_1m_candles_per_coin": TARGET_1M_CANDLES,
            "symbols": symbols,
            "symbol_to_id": symbol_to_id,
            "coins_summary": {
                sym: {
                    "total_samples": coin_data[sym]["sample_count"],
                    "train_samples": coin_data[sym]["train_samples"],
                    "validation_samples": coin_data[sym]["validation_samples"],
                    "test_samples": coin_data[sym]["test_samples"],
                }
                for sym in symbols
            },
            "train_ratio": TRAIN_RATIO,
            "validation_ratio": VALIDATION_RATIO,
            "test_ratio": TEST_RATIO,
            "embargo_minutes": EMBARGO,
            "sequence_length": SEQUENCE_LENGTH,
            "feature_dim": NUM_UNIFIED_FEATURES,
            "sequence_storage": "LAZY_PER_COIN_UNMIXED",
            "normalization_fit": "TRAIN_ONLY_PER_COIN",
        },
    }

    out_dir = os.path.dirname(output_path)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    print(f"\n[DATASET] Saving unified multi-coin bundle to {output_path}...")
    save_start = time.perf_counter()
    torch.save(bundle, output_path)
    save_elapsed = time.perf_counter() - save_start
    file_size_gb = os.path.getsize(output_path) / (1024 ** 3)

    total_elapsed = time.perf_counter() - total_start
    print("\n" + "=" * 80)
    print(" MULTI-COIN DATASET CREATION SUMMARY")
    print("=" * 80)
    print(f"File             : {output_path}")
    print(f"Size             : {file_size_gb:.2f} GiB")
    print(f"Save Time        : {save_elapsed / 60.0:.2f} min")
    print(f"Total Runtime    : {total_elapsed / 60.0:.2f} min ({total_elapsed / 3600.0:.2f} hours)")
    for sym in symbols:
        info = coin_data[sym]
        print(f"  |- {sym:8s}: Train={info['train_samples']:,}  Val={info['validation_samples']:,}  Test={info['test_samples']:,}")
    print("=" * 80)

    return output_path


if __name__ == "__main__":
    generate_multicoin_dataset()
