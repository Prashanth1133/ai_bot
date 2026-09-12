from __future__ import annotations

from typing import Any, Dict
import torch
import torch.nn as nn
from torch.utils.data import DataLoader

from evaluation.metrics import Metrics


class Validator:
    """
    Production Validator evaluating multi-task TradingTransformer outputs:
    - Direction (SELL/HOLD/BUY precision, recall, F1, accuracy)
    - Reversal (accuracy, precision, recall, F1, positive rate)
    - Multi-horizon returns (15m, 1h, 4h)
    - Excursion (max/min 1h)
    - Risk parameters (TP, SL)
    """

    def __init__(
        self,
        model: nn.Module,
        dataloader: DataLoader,
        device: torch.device | None = None,
    ):
        self.model = model
        self.loader = dataloader
        self.device = device or (
            torch.device("cuda" if torch.cuda.is_available() else "cpu")
        )

    @torch.no_grad()
    def validate(self, verbose: bool = True) -> dict[str, Any]:
        self.model.eval()
        self.model.to(self.device)

        all_dir_preds = []
        all_dir_targets = []

        all_rev_preds = []
        all_rev_targets = []

        reg_preds: dict[str, list[float]] = {
            "return_15m": [],
            "return_1h": [],
            "return_4h": [],
            "max_return_1h": [],
            "min_return_1h": [],
            "take_profit": [],
            "stop_loss": [],
        }
        reg_targets: dict[str, list[float]] = {k: [] for k in reg_preds}

        for batch in self.loader:
            if isinstance(batch, (tuple, list)):
                x, y = batch[0], batch[1]
            else:
                x = batch["features"]
                y = batch

            x = x.to(self.device, non_blocking=True)
            outputs = self.model(x)

            # Direction
            if "direction" in outputs and "direction" in y:
                logits = outputs["direction"]
                preds = torch.argmax(logits, dim=-1).cpu().numpy()
                targets = y["direction"].cpu().numpy()
                all_dir_preds.extend(preds)
                all_dir_targets.extend(targets)

            # Reversal
            if "reversal" in outputs and "reversal" in y:
                rev_out = outputs["reversal"]
                if rev_out.shape[-1] == 1:
                    rev_p = torch.sigmoid(rev_out).squeeze(-1).cpu().numpy()
                else:
                    rev_p = torch.argmax(rev_out, dim=-1).cpu().numpy()
                rev_t = y["reversal"].cpu().numpy()
                all_rev_preds.extend(rev_p)
                all_rev_targets.extend(rev_t)

            # Regression keys
            for key in ["return_15m", "return_1h", "return_4h", "max_return_1h", "min_return_1h"]:
                if key in outputs and key in y:
                    p = outputs[key].squeeze(-1).cpu().numpy().tolist()
                    t = y[key].squeeze(-1).cpu().numpy().tolist() if torch.is_tensor(y[key]) else y[key]
                    reg_preds[key].extend(p)
                    reg_targets[key].extend(t)

            # TP/SL keys (handle aliases)
            for out_key, tgt_keys in [("take_profit", ["take_profit", "take_profits", "tp"]),
                                      ("stop_loss", ["stop_loss", "stop_losses", "sl"])]:
                if out_key in outputs:
                    tgt_key = next((k for k in tgt_keys if k in y), None)
                    if tgt_key is not None:
                        p = outputs[out_key].squeeze(-1).cpu().numpy().tolist()
                        t = y[tgt_key].squeeze(-1).cpu().numpy().tolist() if torch.is_tensor(y[tgt_key]) else y[tgt_key]
                        reg_preds[out_key].extend(p)
                        reg_targets[out_key].extend(t)

        # Compute metrics
        direction_metrics = {}
        if all_dir_targets:
            direction_metrics = Metrics.classification_metrics(
                y_true=all_dir_targets,
                y_pred=all_dir_preds,
                num_classes=3,
                class_names=["SELL", "HOLD", "BUY"],
            )

        reversal_metrics = {}
        if all_rev_targets:
            reversal_metrics = Metrics.reversal_metrics(
                y_true=all_rev_targets,
                y_pred=all_rev_preds,
            )

        regression_results = {}
        for key in reg_preds:
            if reg_preds[key]:
                regression_results[key] = Metrics.regression_metrics(
                    y_true=reg_targets[key],
                    y_pred=reg_preds[key],
                )

        if verbose:
            Metrics.print_detailed_summary(
                direction_metrics=direction_metrics,
                reversal_metrics=reversal_metrics if reversal_metrics else None,
                regression_results=regression_results if regression_results else None,
            )

        return {
            "direction": direction_metrics,
            "reversal": reversal_metrics,
            "regression": regression_results,
        }