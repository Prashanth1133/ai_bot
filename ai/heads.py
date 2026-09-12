import torch.nn as nn


class MultiTaskHeads(nn.Module):

    def __init__(
        self,
        d_model: int = 256
    ):
        super().__init__()

        # Direction classification (3 classes: SELL=0, HOLD=1, BUY=2)
        self.direction = nn.Sequential(
            nn.Linear(d_model, 64),
            nn.ReLU(),
            nn.Linear(64, 3)
        )

        # Reversal classification (binary logit)
        self.reversal = nn.Sequential(
            nn.Linear(d_model, 64),
            nn.ReLU(),
            nn.Linear(64, 1)
        )

        # Multi-horizon return regression heads
        self.return_15m = nn.Sequential(
            nn.Linear(d_model, 64),
            nn.ReLU(),
            nn.Linear(64, 1)
        )

        self.return_1h = nn.Sequential(
            nn.Linear(d_model, 64),
            nn.ReLU(),
            nn.Linear(64, 1)
        )

        self.return_4h = nn.Sequential(
            nn.Linear(d_model, 64),
            nn.ReLU(),
            nn.Linear(64, 1)
        )

        # Future excursion regression heads
        self.max_return_1h = nn.Sequential(
            nn.Linear(d_model, 64),
            nn.ReLU(),
            nn.Linear(64, 1)
        )

        self.min_return_1h = nn.Sequential(
            nn.Linear(d_model, 64),
            nn.ReLU(),
            nn.Linear(64, 1)
        )

        # Risk-management targets
        self.take_profit = nn.Sequential(
            nn.Linear(d_model, 64),
            nn.ReLU(),
            nn.Linear(64, 1)
        )

        self.stop_loss = nn.Sequential(
            nn.Linear(d_model, 64),
            nn.ReLU(),
            nn.Linear(64, 1)
        )

    def forward(self, x):
        direction_logits = self.direction(x)
        return {
            "direction": direction_logits,
            "signal_logits": direction_logits,  # Alias for backward compatibility
            "reversal": self.reversal(x),
            "return_15m": self.return_15m(x),
            "return_1h": self.return_1h(x),
            "return_4h": self.return_4h(x),
            "max_return_1h": self.max_return_1h(x),
            "min_return_1h": self.min_return_1h(x),
            "take_profit": self.take_profit(x),
            "stop_loss": self.stop_loss(x),
        }