from __future__ import annotations

from typing import Any
import numpy as np


class DatasetSplitter:
    """
    Purged chronological dataset splitter.

    Enforces a purge gap of (sequence_length + max_horizon) between
    train/val and val/test to prevent sequence overlap and target lookahead leakage.
    """

    def __init__(
        self,
        sequence_length: int = 128,
        max_horizon: int = 240,
    ):
        self.sequence_length = int(sequence_length)
        self.max_horizon = int(max_horizon)
        self.purge_gap = self.sequence_length + self.max_horizon

    def split_indices(
        self,
        total_samples: int,
        train_ratio: float = 0.70,
        validation_ratio: float = 0.15,
        purge_gap: int | None = None,
    ) -> dict[str, tuple[int, int]]:
        gap = self.purge_gap if purge_gap is None else int(purge_gap)
        n = int(total_samples)

        train_start = 0
        train_end = int(n * train_ratio)

        val_start = train_end + gap
        val_end = val_start + int(n * validation_ratio)

        test_start = val_end + gap
        test_end = n

        if test_start >= test_end:
            raise ValueError(
                f"Dataset size ({n}) is too small for purged splitting with gap={gap}. "
                f"Requires at least {val_end + gap + 1} samples."
            )

        return {
            "train": (train_start, train_end),
            "validation": (val_start, val_end),
            "test": (test_start, test_end),
        }

    def split_dict(
        self,
        data_dict: dict[str, Any],
        train_ratio: float = 0.70,
        validation_ratio: float = 0.15,
        purge_gap: int | None = None,
    ) -> dict[str, dict[str, Any]]:
        # Infer length from first key
        first_val = next(iter(data_dict.values()))
        n = len(first_val)

        indices = self.split_indices(
            total_samples=n,
            train_ratio=train_ratio,
            validation_ratio=validation_ratio,
            purge_gap=purge_gap,
        )

        def slice_data(lo: int, hi: int) -> dict[str, Any]:
            sliced = {}
            for k, v in data_dict.items():
                sliced[k] = v[lo:hi]
            return sliced

        return {
            "train": slice_data(*indices["train"]),
            "validation": slice_data(*indices["validation"]),
            "test": slice_data(*indices["test"]),
            "indices": indices,
        }