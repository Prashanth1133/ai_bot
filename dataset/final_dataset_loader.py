from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import numpy as np
import torch
from torch.utils.data import Dataset


class FinalDataset(Dataset):
    """
    Lazy loader for final_unified_dataset.pt.

    Dataset format:

        {
            "train": {
                "features": Tensor[N, 400],
                "direction": Tensor[N],
                "reversal": Tensor[N],
                "return_15m": Tensor[N],
                "return_1h": Tensor[N],
                "return_4h": Tensor[N],
                "max_return_1h": Tensor[N],
                "min_return_1h": Tensor[N],
                "take_profits": Tensor[N],
                "stop_losses": Tensor[N],
                ...
            },

            "validation": {...},
            "test": {...},

            "feature_names": [...],
            "feature_dim": 400,
            "sequence_length": 128,
            "normalization": {...},
            ...
        }

    Windows are generated lazily.

    One returned sample:

        features -> [128, 400]

    No 128-step windows are materialized in RAM.
    """

    REQUIRED_TARGETS = (
        "direction",
        "reversal",
        "return_15m",
        "return_1h",
        "return_4h",
        "max_return_1h",
        "min_return_1h",
        "take_profits",
        "stop_losses",
    )

    SPLITS = {
        "train",
        "validation",
        "test",
    }

    def __init__(
        self,
        dataset_path: str | Path = "dataset/final_unified_dataset_v2.pt",
        split: str = "train",
        symbol: str = "ALL",
        sequence_length: int | None = None,
        normalize: bool = True,
    ):
        self.dataset_path = Path(dataset_path)
        if not self.dataset_path.exists() and Path("dataset/final_unified_dataset.pt").exists():
            self.dataset_path = Path("dataset/final_unified_dataset.pt")

        self.split = split
        self.symbol_filter = symbol
        self.normalize = normalize

        if split not in self.SPLITS:
            raise ValueError(
                f"Invalid split '{split}'. "
                f"Expected one of {sorted(self.SPLITS)}"
            )

        if not self.dataset_path.exists():
            raise FileNotFoundError(
                f"Dataset not found: {self.dataset_path}"
            )

        print(
            f"[FinalDataset] Loading "
            f"{self.dataset_path}"
        )

        self.bundle = torch.load(
            self.dataset_path,
            map_location="cpu",
            weights_only=False,
        )

        # ---------------------------------------------------------
        # Top-level metadata
        # ---------------------------------------------------------

        self.feature_dim = int(
            self.bundle.get("feature_dim", 400)
        )

        self.sequence_length = int(
            sequence_length
            if sequence_length is not None
            else self.bundle.get("sequence_length", 128)
        )

        self.feature_names = self.bundle.get(
            "feature_names",
            [],
        )

        self.metadata = self.bundle.get(
            "metadata",
            {},
        )

        # ---------------------------------------------------------
        # Multi-coin detection
        # ---------------------------------------------------------
        self.is_multicoin = "symbols" in self.bundle and isinstance(self.bundle.get("symbols"), list)
        self.symbols = self.bundle.get("symbols", ["BTCUSDT"])
        self.symbol_to_id = self.bundle.get("symbol_to_id", {s: i for i, s in enumerate(self.symbols)})

        # Prepare per-coin data
        self.coin_stores = {}
        self.index_map = []  # list of (sym_str, sym_id, local_idx)

        if self.is_multicoin:
            target_symbols = self.symbols if symbol == "ALL" else [symbol]
            for sym in target_symbols:
                if sym not in self.bundle:
                    raise KeyError(f"Symbol '{sym}' not in dataset bundle.")
                sym_data = self.bundle[sym][split]
                sym_id = self.symbol_to_id.get(sym, 0)
                store = self._init_store(sym_data, sym, self.bundle[sym].get("normalization", {}))
                self.coin_stores[sym] = store
                n_samples = store["length"]
                for li in range(n_samples):
                    self.index_map.append((sym, sym_id, li))
            self._length = len(self.index_map)
        else:
            # Single coin dataset format
            if split not in self.bundle:
                raise KeyError(
                    f"Dataset does not contain split '{split}'. "
                    f"Available keys: {list(self.bundle.keys())}"
                )
            sym = self.bundle.get("symbol", "BTCUSDT")
            sym_id = 0
            store = self._init_store(self.bundle[split], sym, self.bundle.get("normalization", {}))
            self.coin_stores[sym] = store
            self._length = store["length"]
            for li in range(self._length):
                self.index_map.append((sym, sym_id, li))

        print(
            f"[FinalDataset] {split.upper()} loaded "
            f"(Coins: {list(self.coin_stores.keys())}, Total lazy sequences: {self._length:,})"
        )

    def _init_store(self, split_dict: dict, symbol: str, norm_dict: dict) -> dict:
        features = split_dict.get("features")
        if not torch.is_tensor(features):
            features = torch.as_tensor(features)
        features = features.float()

        n = features.shape[0]
        seq_len = self.sequence_length
        lazy_len = max(0, n - seq_len + 1)

        mean = norm_dict.get("mean")
        std = norm_dict.get("std")
        if mean is not None and not torch.is_tensor(mean):
            mean = torch.as_tensor(mean).float()
        if std is not None and not torch.is_tensor(std):
            std = torch.as_tensor(std).float()

        return {
            "features": features,
            "direction": torch.as_tensor(split_dict["direction"]).long(),
            "reversal": torch.as_tensor(split_dict["reversal"]).float(),
            "return_15m": torch.as_tensor(split_dict["return_15m"]).float(),
            "return_1h": torch.as_tensor(split_dict["return_1h"]).float(),
            "return_4h": torch.as_tensor(split_dict["return_4h"]).float(),
            "max_return_1h": torch.as_tensor(split_dict["max_return_1h"]).float(),
            "min_return_1h": torch.as_tensor(split_dict["min_return_1h"]).float(),
            "take_profits": torch.as_tensor(split_dict.get("take_profits", split_dict.get("take_profit"))).float(),
            "stop_losses": torch.as_tensor(split_dict.get("stop_losses", split_dict.get("stop_loss"))).float(),
            "mean": mean,
            "std": std,
            "length": lazy_len,
            "point_samples": n,
        }

        missing = []

        required_targets = {
            "direction": self.direction,
            "reversal": self.reversal,
            "return_15m": self.return_15m,
            "return_1h": self.return_1h,
            "return_4h": self.return_4h,
            "max_return_1h": self.max_return_1h,
            "min_return_1h": self.min_return_1h,
            "take_profits": self.take_profits,
            "stop_losses": self.stop_losses,
        }

        for name, value in required_targets.items():

            if value is None:
                missing.append(name)

        if missing:

            raise KeyError(
                f"Missing target fields in '{split}': "
                f"{missing}\n"
                f"Available fields: "
                f"{list(self.data.keys())}"
            )

        # ---------------------------------------------------------
        # Convert targets & features
        # ---------------------------------------------------------

        if not torch.is_tensor(self.features):
            self.features = torch.as_tensor(
                self.features
            )

        self.features = self.features.float()

        if self.features.ndim != 2:
            raise ValueError(
                f"Expected point feature matrix "
                f"[N, features], got "
                f"{tuple(self.features.shape)}"
            )

        if self.features.shape[1] != self.feature_dim:
            raise ValueError(
                f"Feature dimension mismatch: "
                f"tensor={self.features.shape[1]}, "
                f"metadata={self.feature_dim}"
            )

        self.direction = torch.as_tensor(
            self.direction
        ).long()

        self.reversal = torch.as_tensor(
            self.reversal
        ).float()

        self.return_15m = torch.as_tensor(
            self.return_15m
        ).float()

        self.return_1h = torch.as_tensor(
            self.return_1h
        ).float()

        self.return_4h = torch.as_tensor(
            self.return_4h
        ).float()

        self.max_return_1h = torch.as_tensor(
            self.max_return_1h
        ).float()

        self.min_return_1h = torch.as_tensor(
            self.min_return_1h
        ).float()

        self.take_profits = torch.as_tensor(
            self.take_profits
        ).float()

        self.stop_losses = torch.as_tensor(
            self.stop_losses
        ).float()

        # ---------------------------------------------------------
        # Target validation
        # ---------------------------------------------------------

        n = self.features.shape[0]

        target_tensors = {
            "direction": self.direction,
            "reversal": self.reversal,
            "return_15m": self.return_15m,
            "return_1h": self.return_1h,
            "return_4h": self.return_4h,
            "max_return_1h": self.max_return_1h,
            "min_return_1h": self.min_return_1h,
            "take_profits": self.take_profits,
            "stop_losses": self.stop_losses,
        }

        for name, tensor in target_tensors.items():

            if tensor.shape[0] != n:

                raise ValueError(
                    f"{split}: {name} length mismatch: "
                    f"{tensor.shape[0]} != {n}"
                )

            if not torch.isfinite(
                tensor.float()
            ).all():

                raise ValueError(
                    f"{split}: {name} contains "
                    f"NaN or Inf"
                )

        # ---------------------------------------------------------
        # Finite checks on features
        # ---------------------------------------------------------

        if not torch.isfinite(
            self.features
        ).all():

            raise ValueError(
                f"{split}: feature matrix contains "
                f"NaN or Inf"
            )

        # ---------------------------------------------------------
        # Direction label validation
        # ---------------------------------------------------------

        unique_labels = torch.unique(
            self.direction
        ).tolist()

        invalid_labels = [
            x for x in unique_labels
            if x not in (0, 1, 2)
        ]

        if invalid_labels:

            raise ValueError(
                f"{split}: invalid direction labels "
                f"{invalid_labels}"
            )

        # ---------------------------------------------------------
        # Normalization
        # ---------------------------------------------------------

        self.mean = None
        self.std = None

        if self.normalize:
            self._load_normalization()

        # ---------------------------------------------------------
        # Lazy sequence count
        # ---------------------------------------------------------

        if n < self.sequence_length:
            self._length = 0
        else:
            self._length = (
                n - self.sequence_length + 1
            )

        print(
            f"[FinalDataset] "
            f"{split.upper()} loaded"
        )

        print(
            f"  Point samples    : {n:,}"
        )

        print(
            f"  Feature dim      : "
            f"{self.feature_dim}"
        )

        print(
            f"  Sequence length  : "
            f"{self.sequence_length}"
        )

        print(
            f"  Lazy sequences   : "
            f"{self._length:,}"
        )

    # =============================================================
    # Internal helpers
    # =============================================================

    def _find_tensor(
        self,
        names: list[str],
    ):

        for name in names:

            if name in self.data:
                return self.data[name]

        return None

    def _load_normalization(self):

        """
        Load train-fitted normalization.

        Validation/test MUST use the same train statistics.
        """

        norm = self.normalization

        if not isinstance(norm, dict):
            return

        mean = None
        std = None

        # Common possible schemas.
        if "mean" in norm:
            mean = norm["mean"]

        if "std" in norm:
            std = norm["std"]

        # Nested feature normalization.
        if "features" in norm:
            feature_norm = norm["features"]

            if isinstance(feature_norm, dict):

                mean = feature_norm.get(
                    "mean",
                    mean,
                )

                std = feature_norm.get(
                    "std",
                    std,
                )

        if mean is None or std is None:
            return

        self.mean = torch.as_tensor(
            mean,
            dtype=torch.float32,
        )

        self.std = torch.as_tensor(
            std,
            dtype=torch.float32,
        )

        if self.mean.numel() != self.feature_dim:
            raise ValueError(
                "Normalization mean dimension "
                f"mismatch: "
                f"{self.mean.numel()} != "
                f"{self.feature_dim}"
            )

        if self.std.numel() != self.feature_dim:
            raise ValueError(
                "Normalization std dimension "
                f"mismatch: "
                f"{self.std.numel()} != "
                f"{self.feature_dim}"
            )

        self.mean = self.mean.reshape(
            1,
            self.feature_dim,
        )

        self.std = self.std.reshape(
            1,
            self.feature_dim,
        )

        # Prevent division by zero for constant features.
        self.std = torch.where(
            self.std.abs() < 1e-8,
            torch.ones_like(self.std),
            self.std,
        )

    # =============================================================
    # Dataset API
    # =============================================================

    def __len__(self):
        return self._length

    def __getitem__(
        self,
        index: int,
    ):
        if index < 0:
            index += self._length

        if index < 0 or index >= self._length:
            raise IndexError(
                f"Index {index} out of range "
                f"for dataset length "
                f"{self._length}"
            )

        sym_str, sym_id, local_start = self.index_map[index]
        store = self.coin_stores[sym_str]
        local_end = local_start + self.sequence_length

        # ---------------------------------------------------------
        # Lazy 128 x 400 window from the specific coin
        # ---------------------------------------------------------
        x = store["features"][local_start:local_end].clone()

        # ---------------------------------------------------------
        # Train-fitted normalization per coin
        # ---------------------------------------------------------
        if (
            self.normalize
            and store["mean"] is not None
            and store["std"] is not None
        ):
            x = (x - store["mean"]) / store["std"]

        # ---------------------------------------------------------
        # Target is associated with final candle of the sequence
        # ---------------------------------------------------------
        target_index = local_end - 1

        return {
            "features": x,
            "symbol": sym_str,
            "symbol_id": torch.tensor(sym_id, dtype=torch.long),

            # Main classification target
            "direction": store["direction"][target_index],

            # Reversal target
            "reversal": store["reversal"][target_index],

            # Multi-horizon regression targets
            "return_15m": store["return_15m"][target_index],
            "return_1h": store["return_1h"][target_index],
            "return_4h": store["return_4h"][target_index],

            # Future excursion targets
            "max_return_1h": store["max_return_1h"][target_index],
            "min_return_1h": store["min_return_1h"][target_index],

            # Risk-management targets
            "take_profit": store["take_profits"][target_index],
            "stop_loss": store["stop_losses"][target_index],
        }

    # =============================================================
    # Metadata
    # =============================================================

    def get_metadata(self) -> dict[str, Any]:
        return {
            "symbols": self.symbols,
            "symbol_to_id": self.symbol_to_id,
            "base_timeframe": self.bundle.get("base_timeframe", "1m"),
            "timeframes": self.bundle.get("timeframes", ["1m", "5m", "15m", "1h", "4h"]),
            "feature_dim": self.feature_dim,
            "sequence_length": self.sequence_length,
            "prediction_horizon_minutes": self.bundle.get("prediction_horizon_minutes", 240),
            "label_version": self.bundle.get("label_version"),
            "dataset_version": self.bundle.get("dataset_version"),
            "feature_names": self.feature_names,
        }


# =================================================================
# SELF TEST
# =================================================================

def self_test(
    dataset_path: str = "dataset/final_unified_dataset_v2.pt",
):
    if not os.path.exists(dataset_path):
        if os.path.exists("dataset/final_unified_dataset_structural_reversal.pt"):
            dataset_path = "dataset/final_unified_dataset_structural_reversal.pt"
        elif os.path.exists("dataset/final_unified_dataset.pt"):
            dataset_path = "dataset/final_unified_dataset.pt"

    print("=" * 70)
    print("FINAL DATASET LOADER SELF-TEST")
    print("=" * 70)

    print(
        f"\nDataset: {dataset_path}"
    )

    for split in (
        "train",
        "validation",
        "test",
    ):
        print(
            f"\n[{split.upper()}]"
        )

        dataset = FinalDataset(
            dataset_path=dataset_path,
            split=split,
            normalize=True,
        )

        print(
            "\nFirst sample:"
        )

        sample = dataset[0]

        print(
            "  symbol       :",
            sample.get("symbol", "N/A"),
            "id=",
            sample.get("symbol_id", torch.tensor(0)).item(),
        )

        print(
            "  features     :",
            tuple(
                sample["features"].shape
            ),
        )

        print(
            "  direction    :",
            sample["direction"].item(),
        )

        print(
            "  reversal     :",
            sample["reversal"].item(),
        )

        print(
            "  return_15m   :",
            sample["return_15m"].item(),
        )

        print(
            "  return_1h    :",
            sample["return_1h"].item(),
        )

        print(
            "  return_4h    :",
            sample["return_4h"].item(),
        )

        print(
            "  max_return_1h:",
            sample["max_return_1h"].item(),
        )

        print(
            "  min_return_1h:",
            sample["min_return_1h"].item(),
        )

        print(
            "  take_profit  :",
            sample["take_profit"].item(),
        )

        print(
            "  stop_loss    :",
            sample["stop_loss"].item(),
        )

        assert sample[
            "features"
        ].shape == (
            128,
            400,
        )

        assert sample[
            "direction"
        ].item() in (
            0,
            1,
            2,
        )

        assert torch.isfinite(
            sample["features"]
        ).all()

        assert torch.isfinite(
            sample["reversal"]
        )

        # Test middle location
        middle = len(dataset) // 2
        sample2 = dataset[middle]
        assert sample2["features"].shape == (128, 400)

        print(
            f"\n  Middle sample index: {middle:,} ({sample2.get('symbol', 'N/A')})"
        )
        print(
            "  Middle shape:",
            tuple(sample2["features"].shape),
        )
        print("  PASS")

    print("\n" + "=" * 70)
    print("FINAL DATASET LOADER SELF-TEST PASSED")
    print("=" * 70)


if __name__ == "__main__":
    self_test()