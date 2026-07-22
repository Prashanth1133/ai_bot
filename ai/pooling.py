import torch
import torch.nn as nn


class AttentionPooling(nn.Module):

    def __init__(
        self,
        d_model
    ):

        super().__init__()

        self.score = nn.Sequential(

            nn.Linear(
                d_model,
                d_model // 2
            ),

            nn.GELU(),

            nn.Linear(
                d_model // 2,
                1
            )

        )

    def forward(self, x):

        weights = torch.softmax(

            self.score(x),

            dim=1

        )

        pooled = torch.sum(

            weights * x,

            dim=1

        )

        return pooled