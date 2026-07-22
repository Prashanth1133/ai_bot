import torch.nn as nn


class MultiTaskHeads(nn.Module):

    def __init__(
        self,
        d_model
    ):

        super().__init__()

        self.direction = nn.Sequential(

            nn.Linear(
                d_model,
                64
            ),

            nn.ReLU(),

            nn.Linear(
                64,
                3
            )

        )

        self.confidence = nn.Sequential(

            nn.Linear(
                d_model,
                64
            ),

            nn.ReLU(),

            nn.Linear(
                64,
                1
            ),

            nn.Sigmoid()

        )

        self.reversal = nn.Sequential(

            nn.Linear(
                d_model,
                64
            ),

            nn.ReLU(),

            nn.Linear(
                64,
                2
            )

        )

        self.volatility = nn.Sequential(

            nn.Linear(
                d_model,
                64
            ),

            nn.ReLU(),

            nn.Linear(
                64,
                1
            )

        )

        self.take_profit = nn.Sequential(

            nn.Linear(
                d_model,
                64
            ),

            nn.ReLU(),

            nn.Linear(
                64,
                1
            )

        )

        self.stop_loss = nn.Sequential(

            nn.Linear(
                d_model,
                64
            ),

            nn.ReLU(),

            nn.Linear(
                64,
                1
            )

        )

        self.market_regime = nn.Sequential(

            nn.Linear(
                d_model,
                64
            ),

            nn.ReLU(),

            nn.Linear(
                64,
                10
            )

        )

    def forward(self, x):

        return {

            "direction":
                self.direction(x),

            "confidence":
                self.confidence(x),

            "reversal":
                self.reversal(x),

            "volatility":
                self.volatility(x),

            "take_profit":
                self.take_profit(x),

            "stop_loss":
                self.stop_loss(x),

            "market_regime":
                self.market_regime(x)

        }