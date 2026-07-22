import torch.nn as nn


class MultiTaskLoss(nn.Module):

    def __init__(self):

        super().__init__()

        self.ce = nn.CrossEntropyLoss()
        self.bce = nn.BCEWithLogitsLoss()
        self.mse = nn.MSELoss()

    def forward(
        self,
        outputs,
        targets
    ):

        direction_loss = self.ce(
            outputs["direction"],
            targets["direction"]
        )

        reversal_loss = self.ce(
            outputs["reversal"],
            targets["reversal"]
        )

        volatility_loss = self.mse(
            outputs["volatility"].squeeze(),
            targets["volatility"]
        )

        total = (
            direction_loss +
            reversal_loss +
            volatility_loss
        )

        return total