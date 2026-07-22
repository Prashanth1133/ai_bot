import torch
import torch.nn as nn


class MultiHeadSelfAttention(nn.Module):

    def __init__(

        self,

        d_model,

        heads

    ):

        super().__init__()

        self.attention = nn.MultiheadAttention(

            d_model,

            heads,

            batch_first=True

        )

    def forward(

        self,

        x

    ):

        out, weights = self.attention(

            x,

            x,

            x,

            need_weights=True

        )

        return out, weights