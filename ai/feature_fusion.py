import torch
import torch.nn as nn


class FeatureFusion(nn.Module):

    def __init__(self, market_dim=128, news_dim=64, onchain_dim=64):
        super().__init__()

        total = market_dim + news_dim + onchain_dim

        self.network = nn.Sequential(
            nn.Linear(total, 256),
            nn.ReLU(),
            nn.Dropout(0.1),
            nn.Linear(256, 256)
        )

    def forward(
        self,
        market_features,
        news_features=None,
        onchain_features=None
    ):

        batch = market_features.size(0)

        if news_features is None:
            news_features = torch.zeros(
                batch,
                64,
                device=market_features.device
            )

        if onchain_features is None:
            onchain_features = torch.zeros(
                batch,
                64,
                device=market_features.device
            )

        x = torch.cat(
            [
                market_features,
                news_features,
                onchain_features
            ],
            dim=-1
        )

        return self.network(x)