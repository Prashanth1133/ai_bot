from __future__ import annotations

import torch
import torch.nn as nn

# Explicit loss weights for multi-task production objective
DIRECTION_WEIGHT: float = 1.00
REVERSAL_WEIGHT: float = 0.50

RETURN_15M_WEIGHT: float = 0.25
RETURN_1H_WEIGHT: float = 0.25
RETURN_4H_WEIGHT: float = 0.25

MAX_RETURN_1H_WEIGHT: float = 0.25
MIN_RETURN_1H_WEIGHT: float = 0.25

TP_WEIGHT: float = 0.50
SL_WEIGHT: float = 0.50


class MultiTaskLoss(nn.Module):
    """
    Production Multi-Task Loss with:
    - Direction: CrossEntropyLoss
    - Reversal: BCEWithLogitsLoss (with optional pos_weight for class imbalance)
    - Returns (15m, 1h, 4h): SmoothL1Loss (beta=0.001)
    - Excursion (max 1h, min 1h): SmoothL1Loss (beta=0.001)
    - Risk (TP, SL): SmoothL1Loss (beta=0.001)
    """

    def __init__(
        self,
        direction_weight: float = DIRECTION_WEIGHT,
        reversal_weight: float = REVERSAL_WEIGHT,
        return_15m_weight: float = RETURN_15M_WEIGHT,
        return_1h_weight: float = RETURN_1H_WEIGHT,
        return_4h_weight: float = RETURN_4H_WEIGHT,
        max_return_1h_weight: float = MAX_RETURN_1H_WEIGHT,
        min_return_1h_weight: float = MIN_RETURN_1H_WEIGHT,
        tp_weight: float = TP_WEIGHT,
        sl_weight: float = SL_WEIGHT,
        reversal_pos_weight: float | torch.Tensor | None = None,
    ):
        super().__init__()

        self.direction_weight = direction_weight
        self.reversal_weight = reversal_weight
        self.return_15m_weight = return_15m_weight
        self.return_1h_weight = return_1h_weight
        self.return_4h_weight = return_4h_weight
        self.max_return_1h_weight = max_return_1h_weight
        self.min_return_1h_weight = min_return_1h_weight
        self.tp_weight = tp_weight
        self.sl_weight = sl_weight

        self.ce = nn.CrossEntropyLoss()

        if reversal_pos_weight is not None:
            if isinstance(reversal_pos_weight, (int, float)):
                reversal_pos_weight = torch.tensor([reversal_pos_weight], dtype=torch.float32)
            self.bce = nn.BCEWithLogitsLoss(pos_weight=reversal_pos_weight)
        else:
            self.bce = nn.BCEWithLogitsLoss()

        # beta=0.001 matches fractional return/excursion scales (std ~ 0.002-0.010)
        self.huber = nn.SmoothL1Loss(beta=0.001)

    def forward(
        self,
        outputs: dict[str, torch.Tensor],
        targets: dict[str, torch.Tensor],
        return_components: bool = False,
    ) -> torch.Tensor | tuple[torch.Tensor, dict[str, float]]:
        # 1. Direction classification loss (3-class: SELL=0, HOLD=1, BUY=2)
        direction_target = targets["direction"].long()
        loss_direction = self.ce(
            outputs["direction"],
            direction_target,
        )

        # 2. Reversal loss (binary classification or multi-class)
        reversal_target = targets["reversal"].float()
        if outputs["reversal"].shape[-1] == 1:
            loss_reversal = self.bce(
                outputs["reversal"].squeeze(-1),
                reversal_target,
            )
        else:
            loss_reversal = self.ce(
                outputs["reversal"],
                reversal_target.long(),
            )

        # 3. Multi-horizon return regression losses (Smooth L1, beta=0.001)
        loss_ret15m = self.huber(
            outputs["return_15m"].squeeze(-1),
            targets["return_15m"].float(),
        )

        loss_ret1h = self.huber(
            outputs["return_1h"].squeeze(-1),
            targets["return_1h"].float(),
        )

        loss_ret4h = self.huber(
            outputs["return_4h"].squeeze(-1),
            targets["return_4h"].float(),
        )

        # 4. Excursion regression losses
        loss_max1h = self.huber(
            outputs["max_return_1h"].squeeze(-1),
            targets["max_return_1h"].float(),
        )

        loss_min1h = self.huber(
            outputs["min_return_1h"].squeeze(-1),
            targets["min_return_1h"].float(),
        )

        # 5. Risk management losses (TP / SL)
        tp_target = targets.get("take_profit", targets.get("take_profits", targets.get("tp"))).float()
        sl_target = targets.get("stop_loss", targets.get("stop_losses", targets.get("sl"))).float()

        loss_tp = self.huber(
            outputs["take_profit"].squeeze(-1),
            tp_target,
        )

        loss_sl = self.huber(
            outputs["stop_loss"].squeeze(-1),
            sl_target,
        )

        total_loss = (
            self.direction_weight * loss_direction
            + self.reversal_weight * loss_reversal
            + self.return_15m_weight * loss_ret15m
            + self.return_1h_weight * loss_ret1h
            + self.return_4h_weight * loss_ret4h
            + self.max_return_1h_weight * loss_max1h
            + self.min_return_1h_weight * loss_min1h
            + self.tp_weight * loss_tp
            + self.sl_weight * loss_sl
        )

        if return_components:
            components = {
                "direction": loss_direction.item(),
                "reversal": loss_reversal.item(),
                "return_15m": loss_ret15m.item(),
                "return_1h": loss_ret1h.item(),
                "return_4h": loss_ret4h.item(),
                "max_return_1h": loss_max1h.item(),
                "min_return_1h": loss_min1h.item(),
                "take_profit": loss_tp.item(),
                "stop_loss": loss_sl.item(),
            }
            return total_loss, components

        return total_loss