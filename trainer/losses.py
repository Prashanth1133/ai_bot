import torch.nn as nn


class TradingLoss(nn.Module):

    def __init__(self):

        super().__init__()

        self.direction = nn.CrossEntropyLoss()

        self.regime = nn.CrossEntropyLoss()

        self.regression = nn.HuberLoss()

        self.binary = nn.BCEWithLogitsLoss()

    def forward(

        self,

        prediction,

        target

    ):

        loss = 0

        loss += self.direction(

            prediction["direction"],

            target["direction"]

        )

        loss += self.regime(

            prediction["regime"],

            target["regime"]

        )

        loss += self.regression(

            prediction["tp"],

            target["tp"]

        )

        loss += self.regression(

            prediction["sl"],

            target["sl"]

        )

        loss += self.binary(

            prediction["confidence"],

            target["confidence"]

        )

        return loss