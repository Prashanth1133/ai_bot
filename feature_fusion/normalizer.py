from __future__ import annotations

from typing import Any
import numpy as np


class FeatureNormalizer:
    """
    Leakage-free Feature Normalizer.

    Calculates mean and standard deviation exclusively on the training partition
    via fit() and transforms train/val/test matrices without lookahead contamination.
    """

    def __init__(self):
        self.mean: np.ndarray | None = None
        self.std: np.ndarray | None = None

    def fit(self, x: np.ndarray) -> FeatureNormalizer:
        arr = np.asarray(x, dtype=np.float64)
        if arr.ndim == 3:
            # Reshape [N, Seq, F] -> [N * Seq, F] for global feature stats
            flat = arr.reshape(-1, arr.shape[-1])
        elif arr.ndim == 2:
            flat = arr
        else:
            raise ValueError(f"Expected 2D or 3D array for normalizer fit, got shape {arr.shape}")

        self.mean = np.nanmean(flat, axis=0)
        self.std = np.nanstd(flat, axis=0)

        # Prevent zero-division on constant or invariant features
        self.std[self.std < 1e-8] = 1.0
        return self

    def transform(self, x: np.ndarray) -> np.ndarray:
        if self.mean is None or self.std is None:
            raise RuntimeError("FeatureNormalizer is not fitted. Call fit() first.")

        orig_shape = x.shape
        arr = np.asarray(x, dtype=np.float32)

        if arr.ndim == 3:
            flat = arr.reshape(-1, arr.shape[-1])
            norm = (flat - self.mean.astype(np.float32)) / self.std.astype(np.float32)
            return norm.reshape(orig_shape)
        elif arr.ndim == 2:
            return (arr - self.mean.astype(np.float32)) / self.std.astype(np.float32)
        else:
            raise ValueError(f"Expected 2D or 3D array for normalizer transform, got shape {arr.shape}")

    def fit_transform(self, x: np.ndarray) -> np.ndarray:
        self.fit(x)
        return self.transform(x)

    def normalize(self, vector: Any) -> Any:
        """Online pass-through helper for dict/vector structures."""
        if isinstance(vector, dict):
            result = {}
            for k, v in vector.items():
                if isinstance(v, (int, float)):
                    result[k] = float(v)
                else:
                    result[k] = v
            return result
        return vector