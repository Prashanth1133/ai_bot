from __future__ import annotations

import numpy as np


class LeakageChecker:

    @staticmethod
    def check_feature_matrix(
        features,
        expected_features: int | None = None,
    ):
        x = np.asarray(
            features,
            dtype=np.float32,
        )

        # Final dataset stores POINT FEATURES:
        # [N, FEATURES]
        #
        # Training creates:
        # [N, SEQUENCE_LENGTH, FEATURES]
        #
        # Therefore both representations are valid here.
        if x.ndim not in (2, 3):
            raise ValueError(
                f"Expected 2D point matrix or 3D sequence tensor, "
                f"got {x.ndim}D"
            )

        if not np.isfinite(x).all():
            raise ValueError(
                "Dataset contains NaN or Inf."
            )

        if x.ndim == 2:
            n_samples, n_features = x.shape

            if n_samples <= 0:
                raise ValueError(
                    "Dataset contains zero samples."
                )

            if n_features <= 0:
                raise ValueError(
                    "Dataset contains zero features."
                )

            if (
                expected_features is not None
                and n_features != expected_features
            ):
                raise ValueError(
                    f"Expected {expected_features} features, "
                    f"got {n_features}"
                )

        else:
            n_samples, sequence_length, n_features = x.shape

            if n_samples <= 0:
                raise ValueError(
                    "Dataset contains zero samples."
                )

            if sequence_length <= 0:
                raise ValueError(
                    "Dataset contains zero sequence length."
                )

            if n_features <= 0:
                raise ValueError(
                    "Dataset contains zero features."
                )

            if (
                expected_features is not None
                and n_features != expected_features
            ):
                raise ValueError(
                    f"Expected {expected_features} features, "
                    f"got {n_features}"
                )

        return True

    @staticmethod
    def check_labels(
        labels,
        n_samples,
    ):
        labels = np.asarray(labels)

        if len(labels) != n_samples:
            raise ValueError(
                f"Label/sample mismatch: "
                f"{len(labels)} labels for {n_samples} samples."
            )

        if not np.isfinite(
            labels.astype(np.float64)
        ).all():
            raise ValueError(
                "Invalid labels."
            )

        valid = {0, 1, 2}

        found = set(
            np.unique(labels).tolist()
        )

        if not found.issubset(valid):
            raise ValueError(
                f"Invalid direction labels: {found}"
            )

        return True