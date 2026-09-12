from __future__ import annotations

from typing import Any
import numpy as np


class DatasetStatistics:

    @staticmethod
    def summarize(features: Any) -> dict[str, Any]:
        x = np.asarray(features, dtype=np.float64)

        if x.ndim == 3:
            flat = x.reshape(-1, x.shape[-1])
        elif x.ndim == 2:
            flat = x
        else:
            raise ValueError("Expected 2D or 3D features.")

        return {
            "rows": int(flat.shape[0]),
            "columns": int(flat.shape[1]),
            "mean": np.nanmean(flat, axis=0),
            "std": np.nanstd(flat, axis=0),
            "min": np.nanmin(flat, axis=0),
            "max": np.nanmax(flat, axis=0),
        }