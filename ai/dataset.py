from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import torch
from torch.utils.data import Dataset


class ChronologicalUnifiedDataset(Dataset):
    """
    Dataset wrapper for production chronological partitions from final_unified_dataset_v7.pt.
    Provides [128, 48] feature windows and multi-task target dictionaries.
    """

    def __init__(
        self,
        features: torch.Tensor,
        targets: dict[str, torch.Tensor],
    ):
        self.features = features.float()
        self.targets = targets

    def __len__(self) -> int:
        return len(self.features)

    def __getitem__(self, idx: int) -> tuple[torch.Tensor, dict[str, torch.Tensor]]:
        x = self.features[idx]
        y = {k: v[idx] for k, v in self.targets.items()}
        return x, y


def load_chronological_datasets(
    dataset_path: str | Path = "dataset/final_unified_dataset_v7.pt",
) -> tuple[ChronologicalUnifiedDataset, ChronologicalUnifiedDataset, ChronologicalUnifiedDataset]:
    """
    Loads final_unified_dataset_v7.pt and slices Train, Validation, and Test partitions
    according to pre-defined chronological boundaries, preserving purge gaps.
    """
    path = Path(dataset_path)
    if not path.exists():
        raise FileNotFoundError(f"Dataset file not found at: {path}")

    bundle = torch.load(path, map_location="cpu", weights_only=False)

    sequences = bundle["sequences"]
    splits = bundle["splits"]

    # Target fields dictionary
    targets = {
        "direction": bundle["labels"].long(),
        "reversal": bundle["reversals"].float(),
        "regime": bundle["regimes"].long(),
        "return_15m": bundle["future_return_15m"].float(),
        "return_1h": bundle["future_return_1h"].float(),
        "return_4h": bundle["future_return_4h"].float(),
        "max_return_1h": bundle["max_future_return_1h"].float(),
        "min_return_1h": bundle["min_future_return_1h"].float(),
        "take_profit": bundle["take_profits"].float(),
        "stop_loss": bundle["stop_losses"].float(),
    }

    train_start, train_end = splits["train"]
    val_start, val_end = splits["validation"]
    test_start, test_end = splits["test"]

    train_feats = sequences[train_start:train_end]
    train_targets = {k: v[train_start:train_end] for k, v in targets.items()}

    val_feats = sequences[val_start:val_end]
    val_targets = {k: v[val_start:val_end] for k, v in targets.items()}

    test_feats = sequences[test_start:test_end]
    test_targets = {k: v[test_start:test_end] for k, v in targets.items()}

    train_ds = ChronologicalUnifiedDataset(train_feats, train_targets)
    val_ds = ChronologicalUnifiedDataset(val_feats, val_targets)
    test_ds = ChronologicalUnifiedDataset(test_feats, test_targets)

    print(f"\n[DATASET LOADER] Loaded {path.name}:")
    print(f"  Train samples     : {len(train_ds):,} [{train_start}..{train_end}]")
    print(f"  Purge 1           : {splits.get('purge_gap', 368):,} [{splits['purge_1'][0]}..{splits['purge_1'][1]}]")
    print(f"  Validation samples: {len(val_ds):,} [{val_start}..{val_end}]")
    print(f"  Purge 2           : {splits.get('purge_gap', 368):,} [{splits['purge_2'][0]}..{splits['purge_2'][1]}]")
    print(f"  Test samples      : {len(test_ds):,} [{test_start}..{test_end}] (UNTOUCHED)")

    return train_ds, val_ds, test_ds


class TradingDataset(Dataset):
    """
    Legacy sequence dataset wrapper maintained for backwards compatibility.
    """

    def __init__(self, features, labels):
        self.features = features
        self.labels = labels

    def __len__(self):
        return len(self.features)

    def __getitem__(self, idx):
        x = torch.tensor(self.features[idx], dtype=torch.float32)
        y = {
            "direction": torch.tensor(self.labels[idx]["direction"], dtype=torch.long),
            "confidence": torch.tensor(self.labels[idx].get("confidence", 1.0), dtype=torch.float32),
            "reversal": torch.tensor(self.labels[idx]["reversal"], dtype=torch.long),
            "volatility": torch.tensor(self.labels[idx].get("volatility", 0.0), dtype=torch.float32),
            "take_profit": torch.tensor(self.labels[idx]["take_profit"], dtype=torch.float32),
            "stop_loss": torch.tensor(self.labels[idx]["stop_loss"], dtype=torch.float32),
            "market_regime": torch.tensor(self.labels[idx].get("market_regime", 1), dtype=torch.long),
        }
        return x, y