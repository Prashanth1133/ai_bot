from __future__ import annotations

import numpy as np


class FeatureNormalizer:
    def __init__(self):
        self.mean = None
        self.std = None

    def fit(
        self,
        x: np.ndarray,
    ):
        flat = x.reshape(
            -1,
            x.shape[-1],
        )

        self.mean = np.mean(
            flat,
            axis=0,
            keepdims=True,
        )

        self.std = np.std(
            flat,
            axis=0,
            keepdims=True,
        )

        self.std[
            self.std < 1e-8
        ] = 1.0

        return self

    def transform(
        self,
        x: np.ndarray,
    ):
        if self.mean is None:
            raise RuntimeError(
                "Normalizer has not been fitted."
            )

        return (
            x - self.mean
        ) / self.std

    def fit_transform(
        self,
        x: np.ndarray,
    ):
        self.fit(x)

        return self.transform(x)

    def state_dict(self):
        return {
            "mean": self.mean,
            "std": self.std,
        }
