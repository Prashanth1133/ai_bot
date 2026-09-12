from __future__ import annotations

from typing import Any, Dict
import torch
import numpy as np


class Metrics:
    """
    Comprehensive evaluation metrics for the CryptoVisionAI multi-task model:
    - Direction (3-class: SELL=0, HOLD=1, BUY=2) precision, recall, F1, accuracy
    - Reversal (binary) accuracy, precision, recall, F1
    - Multi-horizon returns (15m, 1h, 4h) regression errors
    - Excursion (max/min 1h) regression errors
    - Risk parameters (TP, SL) regression errors
    """

    @staticmethod
    def classification_metrics(
        y_true: torch.Tensor | np.ndarray | list,
        y_pred: torch.Tensor | np.ndarray | list,
        num_classes: int = 3,
        class_names: list[str] | None = None,
    ) -> dict[str, Any]:
        if isinstance(y_true, torch.Tensor):
            y_true = y_true.detach().cpu().numpy()
        else:
            y_true = np.asarray(y_true)

        if isinstance(y_pred, torch.Tensor):
            y_pred = y_pred.detach().cpu().numpy()
        else:
            y_pred = np.asarray(y_pred)

        if y_pred.ndim > 1 and y_pred.shape[-1] == num_classes:
            y_pred = np.argmax(y_pred, axis=-1)

        y_true = y_true.astype(int).ravel()
        y_pred = y_pred.astype(int).ravel()

        if class_names is None:
            if num_classes == 3:
                class_names = ["SELL", "HOLD", "BUY"]
            else:
                class_names = [f"Class_{i}" for i in range(num_classes)]

        total_samples = len(y_true)
        accuracy = float(np.mean(y_true == y_pred)) if total_samples > 0 else 0.0

        per_class: dict[str, dict[str, float]] = {}
        f1_list = []

        for idx, name in enumerate(class_names):
            tp = int(np.sum((y_true == idx) & (y_pred == idx)))
            fp = int(np.sum((y_true != idx) & (y_pred == idx)))
            fn = int(np.sum((y_true == idx) & (y_pred != idx)))
            support = int(np.sum(y_true == idx))

            prec = tp / (tp + fp) if (tp + fp) > 0 else 0.0
            rec = tp / (tp + fn) if (tp + fn) > 0 else 0.0
            f1 = 2 * (prec * rec) / (prec + rec) if (prec + rec) > 0 else 0.0

            per_class[name] = {
                "precision": float(prec),
                "recall": float(rec),
                "f1": float(f1),
                "support": support,
            }
            f1_list.append(f1)

        macro_f1 = float(np.mean(f1_list)) if f1_list else 0.0

        return {
            "accuracy": accuracy,
            "macro_f1": macro_f1,
            "total_samples": total_samples,
            "per_class": per_class,
        }

    @staticmethod
    def reversal_metrics(
        y_true: torch.Tensor | np.ndarray | list,
        y_pred: torch.Tensor | np.ndarray | list,
        threshold: float = 0.50,
    ) -> dict[str, float]:
        if isinstance(y_true, torch.Tensor):
            y_true = y_true.detach().cpu().numpy()
        else:
            y_true = np.asarray(y_true)

        if isinstance(y_pred, torch.Tensor):
            y_pred = y_pred.detach().cpu().numpy()
        else:
            y_pred = np.asarray(y_pred)

        y_true = y_true.ravel()
        y_pred = y_pred.ravel()

        if y_pred.dtype.kind == 'f':
            # probabilities or logits
            if np.min(y_pred) < 0 or np.max(y_pred) > 1:
                # Logits -> sigmoid
                y_pred_prob = 1.0 / (1.0 + np.exp(-y_pred))
            else:
                y_pred_prob = y_pred
            y_pred_bin = (y_pred_prob >= threshold).astype(int)
        else:
            y_pred_bin = y_pred.astype(int)

        y_true_bin = (y_true >= 0.5).astype(int)

        tp = int(np.sum((y_true_bin == 1) & (y_pred_bin == 1)))
        fp = int(np.sum((y_true_bin == 0) & (y_pred_bin == 1)))
        fn = int(np.sum((y_true_bin == 1) & (y_pred_bin == 0)))
        tn = int(np.sum((y_true_bin == 0) & (y_pred_bin == 0)))

        acc = (tp + tn) / max(len(y_true_bin), 1)
        prec = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        rec = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        f1 = 2 * (prec * rec) / (prec + rec) if (prec + rec) > 0 else 0.0
        pos_rate = float(np.mean(y_true_bin)) if len(y_true_bin) > 0 else 0.0

        return {
            "accuracy": float(acc),
            "precision": float(prec),
            "recall": float(rec),
            "f1": float(f1),
            "positive_rate": pos_rate,
        }

    @staticmethod
    def regression_metrics(
        y_true: torch.Tensor | np.ndarray | list,
        y_pred: torch.Tensor | np.ndarray | list,
    ) -> dict[str, float]:
        if isinstance(y_true, torch.Tensor):
            y_true = y_true.detach().cpu().numpy()
        else:
            y_true = np.asarray(y_true)

        if isinstance(y_pred, torch.Tensor):
            y_pred = y_pred.detach().cpu().numpy()
        else:
            y_pred = np.asarray(y_pred)

        y_true = y_true.ravel()
        y_pred = y_pred.ravel()

        diff = y_pred - y_true
        mae = float(np.mean(np.abs(diff)))
        mse = float(np.mean(diff ** 2))
        rmse = float(np.sqrt(mse))

        # Smooth L1 (beta=0.001)
        abs_diff = np.abs(diff)
        smooth_l1 = np.where(abs_diff < 0.001, 0.5 * (abs_diff ** 2) / 0.001, abs_diff - 0.5 * 0.001)
        smooth_l1_val = float(np.mean(smooth_l1))

        return {
            "mae": mae,
            "mse": mse,
            "rmse": rmse,
            "smooth_l1": smooth_l1_val,
        }

    # Backward compatibility helpers
    @staticmethod
    def direction_accuracy(prediction: torch.Tensor, target: torch.Tensor) -> float:
        if prediction.ndim > 1:
            prediction = torch.argmax(prediction, dim=-1)
        return float((prediction == target).sum().item() / max(len(target), 1))

    @staticmethod
    def reversal_accuracy(prediction: torch.Tensor, target: torch.Tensor) -> float:
        if prediction.ndim > 1 and prediction.shape[-1] > 1:
            prediction = torch.argmax(prediction, dim=-1)
        elif prediction.ndim > 1:
            prediction = (torch.sigmoid(prediction) >= 0.5).long().squeeze(-1)
        return float((prediction == target).sum().item() / max(len(target), 1))

    @staticmethod
    def mse(prediction: torch.Tensor, target: torch.Tensor) -> float:
        return float(((prediction - target) ** 2).mean().item())

    @staticmethod
    def print_detailed_summary(
        direction_metrics: dict[str, Any],
        reversal_metrics: dict[str, float] | None = None,
        regression_results: dict[str, dict[str, float]] | None = None,
    ) -> None:
        print("\n" + "=" * 60)
        print(" PRODUCTION EVALUATION SUMMARY")
        print("=" * 60)

        print("\n[DIRECTION CLASSIFICATION]")
        print(f"  Overall Accuracy : {direction_metrics.get('accuracy', 0.0) * 100:.2f}%")
        print(f"  Macro F1 Score   : {direction_metrics.get('macro_f1', 0.0):.4f}")
        print("  Per-Class Breakdown:")

        per_class = direction_metrics.get("per_class", {})
        for name, stats in per_class.items():
            print(
                f"    {name:<6} -> Precision: {stats['precision']:.4f} | "
                f"Recall: {stats['recall']:.4f} | F1: {stats['f1']:.4f} | "
                f"Support: {stats['support']:,}"
            )

        if reversal_metrics:
            print("\n[REVERSAL CLASSIFICATION]")
            print(f"  Accuracy         : {reversal_metrics.get('accuracy', 0.0) * 100:.2f}%")
            print(f"  Precision        : {reversal_metrics.get('precision', 0.0):.4f}")
            print(f"  Recall           : {reversal_metrics.get('recall', 0.0):.4f}")
            print(f"  F1 Score         : {reversal_metrics.get('f1', 0.0):.4f}")
            print(f"  Dataset Positive : {reversal_metrics.get('positive_rate', 0.0) * 100:.2f}%")

        if regression_results:
            print("\n[MULTI-TASK REGRESSION]")
            for target_name, stats in regression_results.items():
                print(
                    f"    {target_name:<16} -> SmoothL1: {stats['smooth_l1']:.6f} | "
                    f"MAE: {stats['mae']:.6f} | RMSE: {stats['rmse']:.6f}"
                )
        print("=" * 60 + "\n")