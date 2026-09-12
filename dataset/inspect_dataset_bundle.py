from __future__ import annotations

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import numpy as np
import torch

from feature_fusion.schema import (
    UNIFIED_FEATURE_SCHEMA,
    NUM_UNIFIED_FEATURES,
)


def inspect_dataset(
    dataset_path=None
):
    if dataset_path is None:
        if os.path.exists("dataset/final_unified_dataset_v7.pt"):
            dataset_path = "dataset/final_unified_dataset_v7.pt"
        else:
            dataset_path = "dataset/final_unified_dataset_v6.pt"

    print("=" * 70)
    print(f"FINAL DATASET FORENSIC AUDIT ({dataset_path})")
    print("=" * 70)

    if not os.path.exists(dataset_path):
        raise FileNotFoundError(dataset_path)

    data = torch.load(
        dataset_path,
        map_location="cpu",
        weights_only=False,
    )

    if "sequences" in data:
        sequences = data["sequences"]
        labels = data.get("labels")
    elif "train" in data and isinstance(data["train"], dict):
        # Flatten splits or inspect train
        features_list = []
        labels_list = []
        for s in ("train", "validation", "test"):
            if s in data:
                if "sequences" in data[s]:
                    features_list.append(data[s]["sequences"])
                elif "features" in data[s]:
                    features_list.append(data[s]["features"])
                if "labels" in data[s]:
                    labels_list.append(data[s]["labels"])
                elif "direction" in data[s]:
                    labels_list.append(data[s]["direction"])
        sequences = torch.cat(features_list, dim=0) if features_list else None
        labels = torch.cat(labels_list, dim=0) if labels_list else None
    else:
        raise KeyError(f"Unrecognized dataset structure. Keys: {list(data.keys())}")

    print(
        "Dataset version :",
        data.get("dataset_version", "UNKNOWN"),
    )
    print(
        "Feature version :",
        data.get("feature_version", "UNKNOWN"),
    )
    print(
        "Label version   :",
        data.get("label_version", "UNKNOWN"),
    )

    print()
    print("DATASET SIZE")
    print("Samples  :", sequences.shape[0] if sequences is not None else "N/A")
    print("Shape    :", sequences.shape if sequences is not None else "N/A")

    # ---------------------------------------------------------
    # FINITE & SHAPE
    # ---------------------------------------------------------
    if sequences is not None:
        assert torch.isfinite(sequences).all()
        num_features = int(sequences.shape[-1])
        if num_features != NUM_UNIFIED_FEATURES:
            raise RuntimeError(
                f"Feature dimension mismatch: "
                f"dataset={num_features}, "
                f"schema={NUM_UNIFIED_FEATURES}"
            )
        flat = sequences.numpy().reshape(-1, num_features)
    else:
        raise ValueError("No feature sequences found to inspect.")

    # ---------------------------------------------------------
    # FEATURE AUDIT
    # ---------------------------------------------------------
    print()
    print("=" * 70)
    print(f"{num_features} FEATURE AUDIT")
    print("=" * 70)

    constant = []

    for i, name in enumerate(UNIFIED_FEATURE_SCHEMA):
        col = flat[:, i]
        minimum = float(np.min(col))
        maximum = float(np.max(col))
        mean = float(np.mean(col))
        std = float(np.std(col))
        status = "DYNAMIC" if std > 1e-8 else "CONSTANT"

        print(
            f"{i:02d} "
            f"{name:<35} "
            f"min={minimum:>12.6f} "
            f"max={maximum:>12.6f} "
            f"mean={mean:>12.6f} "
            f"std={std:>12.6f} "
            f"{status}"
        )

        if status == "CONSTANT":
            constant.append(name)

    print()
    if constant:
        print("CONSTANT FEATURES:")
        for name in constant:
            print("  ", name)
        raise RuntimeError("AUDIT FAILED: all 48 features must be dynamic.")

    print("48/48 FEATURES DYNAMIC: PASS")

    # ---------------------------------------------------------
    # EVENT FEATURE SEMANTIC AUDIT
    # ---------------------------------------------------------
    print()
    print("=" * 70)
    print("EVENT FEATURE SEMANTIC AUDIT")
    print("=" * 70)
    event_features = ["breakout_flag", "breakdown_flag", "smc_bos_flag", "smc_choch_flag"]
    for name in event_features:
        if name in UNIFIED_FEATURE_SCHEMA:
            idx = UNIFIED_FEATURE_SCHEMA.index(name)
            col = flat[:, idx]
            active_ratio = float((col > 0.5).mean())
            active_count = int((col > 0.5).sum())
            status = "PASS (SPARSE EVENT)" if active_ratio <= 0.20 else "FAIL (SATURATED)"
            print(f"{name:<30s} active={active_ratio * 100:7.3f}% | count={active_count:>8,} | {status}")
            if active_ratio > 0.20:
                raise RuntimeError(f"AUDIT FAILED: {name} is saturated ({active_ratio:.2%})")

    # ---------------------------------------------------------
    # S/R STRENGTH & TOUCH AUDIT
    # ---------------------------------------------------------
    print()
    print("=" * 70)
    print("S/R STRENGTH & TOUCH DISTRIBUTION AUDIT")
    print("=" * 70)
    strength_features = ["support_strength", "resistance_strength"]
    for name in strength_features:
        if name in UNIFIED_FEATURE_SCHEMA:
            idx = UNIFIED_FEATURE_SCHEMA.index(name)
            col = flat[:, idx]
            mean = float(np.mean(col))
            std = float(np.std(col))
            p05 = float(np.percentile(col, 5))
            p50 = float(np.percentile(col, 50))
            p95 = float(np.percentile(col, 95))
            status = "PASS" if std >= 0.02 else "FAIL"
            print(f"{name:<30s} mean={mean:.4f} std={std:.4f} | p05={p05:.4f} p50={p50:.4f} p95={p95:.4f} | {status}")
            if std < 0.02:
                raise RuntimeError(f"AUDIT FAILED: {name} std={std:.6f} < 0.02")

    touch_features = ["touch_count_support", "touch_count_resistance"]
    for name in touch_features:
        if name in UNIFIED_FEATURE_SCHEMA:
            idx = UNIFIED_FEATURE_SCHEMA.index(name)
            col = flat[:, idx]
            mean = float(np.mean(col))
            max_v = float(np.max(col))
            p50 = float(np.percentile(col, 50))
            p95 = float(np.percentile(col, 95))
            status = "PASS" if mean <= 20.0 else "FAIL"
            print(f"{name:<30s} mean={mean:.3f} max={max_v:.1f} | median={p50:.1f} p95={p95:.1f} | {status}")
            if mean > 20.0:
                raise RuntimeError(f"AUDIT FAILED: {name} mean={mean:.2f} > 20.0")

    # ---------------------------------------------------------
    # LABEL DISTRIBUTION (DIRECTION, REVERSAL, REGIME)
    # ---------------------------------------------------------
    print()
    print("=" * 70)
    print("DIRECTION TARGET DISTRIBUTION")
    print("=" * 70)

    unique, counts = np.unique(
        labels.numpy(),
        return_counts=True,
    )
    total = len(labels)

    for label, count in zip(unique, counts):
        label_name = {0: "SELL", 1: "HOLD", 2: "BUY"}.get(int(label), f"LABEL_{label}")
        print(f"{label_name:<8} ({label}): {count:,} ({count / total * 100:.2f}%)")

    if "reversals" in data and data["reversals"] is not None:
        revs = data["reversals"].numpy()
        u_rev, c_rev = np.unique(revs, return_counts=True)
        print()
        print("REVERSAL TARGET DISTRIBUTION")
        print("-" * 50)
        for r, c in zip(u_rev, c_rev):
            r_name = "REVERSAL" if r > 0.5 else "NO_REVERSAL"
            print(f"{r_name:<15} ({r:.0f}): {c:>6,} ({c / len(revs) * 100:>6.2f}%)")

    if "regimes" in data and data["regimes"] is not None:
        regs = data["regimes"].numpy()
        u_reg, c_reg = np.unique(regs, return_counts=True)
        print()
        print("REGIME TARGET DISTRIBUTION")
        print("-" * 50)
        for r, c in zip(u_reg, c_reg):
            reg_name = {0: "BEAR", 1: "RANGE", 2: "BULL"}.get(int(r), f"REGIME_{r}")
            print(f"{reg_name:<15} ({r}): {c:>6,} ({c / len(regs) * 100:>6.2f}%)")

    # ---------------------------------------------------------
    # TIMESTAMPS
    # ---------------------------------------------------------
    if "timestamps" in data:
        timestamps = data["timestamps"].numpy()
        if not np.all(np.diff(timestamps) > 0):
            raise RuntimeError("Timestamp ordering failed")
        print()
        print("Timestamp ordering: PASS")

    # ---------------------------------------------------------
    # SPLITS
    # ---------------------------------------------------------
    if "splits" in data:
        splits = data["splits"]
        print()
        for k in ("train", "purge_1", "validation", "purge_2", "test", "purge_gap"):
            if k in splits:
                v = splits[k]
                if isinstance(v, (list, tuple)) and len(v) == 2:
                    print(f"{k.upper():<12}: [{v[0]:>6,} .. {v[1]:>6,}] ({v[1] - v[0]:>6,} samples)")
                else:
                    print(f"{k.upper():<12}: {v}")

    print()
    print("=" * 70)
    print("FORENSIC AUDIT: 100% PASSED")
    print("=" * 70)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Inspect dataset bundle")
    parser.add_argument("--path", type=str, default=None)
    args = parser.parse_args()
    inspect_dataset(args.path)
