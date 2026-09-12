from __future__ import annotations

import os
import numpy as np
import torch


DEFAULT_PATH = "dataset/final_unified_dataset_v3.pt"


def _tensor(data, *keys):
    for key in keys:
        if key in data:
            return data[key]

    return None


def _collect_split(data, key):
    values = []

    for split_name in ("train", "validation", "test"):
        split = data.get(split_name, {})

        value = split.get(key)

        if value is not None:
            values.append(value.detach().cpu())

    if not values:
        return None

    return torch.cat(values, dim=0)


def audit(path: str = DEFAULT_PATH):

    print("=" * 70)
    print("FINAL DATASET LABEL AUDIT")
    print("=" * 70)

    print(f"\nDataset: {path}")

    if not os.path.exists(path):
        print("\n[WAITING]")
        print("Dataset does not exist yet.")
        print("This is expected before final dataset generation.")
        print("\nGenerate the dataset first, then run this audit.")
        return False

    data = torch.load(
        path,
        map_location="cpu",
        weights_only=False,
    )

    print("\nDataset loaded successfully.")

    # ---------------------------------------------------------
    # VERSION
    # ---------------------------------------------------------

    print("\n" + "=" * 60)
    print("VERSION")
    print("=" * 60)

    print(
        "Dataset version:",
        data.get("dataset_version", "UNKNOWN"),
    )

    print(
        "Label version:",
        data.get("label_version", "UNKNOWN"),
    )

    # ---------------------------------------------------------
    # DIRECTION
    # ---------------------------------------------------------

    direction = _collect_split(
        data,
        "direction",
    )

    if direction is None:

        direction = _tensor(
            data,
            "labels",
            "direction",
        )

    if direction is None:

        print("\n[FAIL] Direction labels not found.")
        return False

    direction = direction.numpy()

    print("\n" + "=" * 60)
    print("DIRECTION LABELS")
    print("=" * 60)

    unique, counts = np.unique(
        direction,
        return_counts=True,
    )

    total = len(direction)

    names = {
        0: "SELL",
        1: "HOLD",
        2: "BUY",
    }

    for label, count in zip(unique, counts):

        name = names.get(
            int(label),
            "UNKNOWN",
        )

        pct = (
            count /
            max(total, 1)
            * 100
        )

        print(
            f"{name:<8} : "
            f"{count:>10,} "
            f"({pct:6.2f}%)"
        )

    if not set(unique).issubset({0, 1, 2}):

        print(
            "\n[FAIL] Invalid direction labels."
        )

        return False

    # ---------------------------------------------------------
    # REVERSAL
    # ---------------------------------------------------------

    reversal = _collect_split(
        data,
        "reversal",
    )

    if reversal is None:

        reversal = _tensor(
            data,
            "reversals",
        )

    if reversal is None:

        print(
            "\n[FAIL] Reversal labels not found."
        )

        return False

    reversal = reversal.numpy()

    reversal = np.asarray(
        reversal,
        dtype=np.float32,
    )

    print("\n" + "=" * 60)
    print("REVERSAL LABELS")
    print("=" * 60)

    unique, counts = np.unique(
        reversal,
        return_counts=True,
    )

    total = len(reversal)

    for label, count in zip(unique, counts):

        pct = (
            count /
            max(total, 1)
            * 100
        )

        name = (
            "NO REVERSAL"
            if float(label) == 0.0
            else "REVERSAL"
        )

        print(
            f"{name:<15} : "
            f"{count:>10,} "
            f"({pct:6.2f}%)"
        )

    # ---------------------------------------------------------
    # VALIDITY
    # ---------------------------------------------------------

    valid_values = np.isin(
        reversal,
        [0.0, 1.0],
    )

    if not valid_values.all():

        print(
            "\n[FAIL] Reversal contains "
            "values other than 0/1."
        )

        return False

    reversal_rate = (
        np.mean(reversal > 0.5)
        if len(reversal)
        else 0.0
    )

    print(
        f"\nReversal rate : "
        f"{reversal_rate * 100:.2f}%"
    )

    # ---------------------------------------------------------
    # EXTREME DISTRIBUTION PROTECTION
    # ---------------------------------------------------------

    if reversal_rate > 0.50:

        print(
            "\n[FAIL] Reversal rate exceeds 50%."
        )

        print(
            "The structural reversal label "
            "is still too permissive."
        )

        return False

    if reversal_rate < 0.001:

        print(
            "\n[WARNING] Reversal rate is "
            "extremely low."
        )

    # ---------------------------------------------------------
    # TP
    # ---------------------------------------------------------

    tp = _collect_split(
        data,
        "take_profits",
    )

    if tp is not None:

        tp = tp.numpy()

        print("\n" + "=" * 60)
        print("TAKE PROFIT")
        print("=" * 60)

        print(
            "Min :",
            float(np.min(tp)),
        )

        print(
            "Max :",
            float(np.max(tp)),
        )

        print(
            "Mean:",
            float(np.mean(tp)),
        )

        if not np.isfinite(tp).all():

            print("[FAIL] TP contains NaN/Inf.")
            return False

        if np.any(tp <= 0):

            print(
                "[FAIL] TP contains "
                "non-positive values."
            )

            return False

    # ---------------------------------------------------------
    # SL
    # ---------------------------------------------------------

    sl = _collect_split(
        data,
        "stop_losses",
    )

    if sl is not None:

        sl = sl.numpy()

        print("\n" + "=" * 60)
        print("STOP LOSS")
        print("=" * 60)

        print(
            "Min :",
            float(np.min(sl)),
        )

        print(
            "Max :",
            float(np.max(sl)),
        )

        print(
            "Mean:",
            float(np.mean(sl)),
        )

        if not np.isfinite(sl).all():

            print("[FAIL] SL contains NaN/Inf.")
            return False

        if np.any(sl <= 0):

            print(
                "[FAIL] SL contains "
                "non-positive values."
            )

            return False

    # ---------------------------------------------------------
    # FINAL
    # ---------------------------------------------------------

    print("\n" + "=" * 70)
    print("LABEL AUDIT RESULT")
    print("=" * 70)

    print("Direction labels : PASS")
    print("Reversal labels  : PASS")
    print("TP labels        : PASS")
    print("SL labels        : PASS")

    print("\nREADY FOR FINAL DATASET VALIDATION")

    return True


if __name__ == "__main__":

    audit()