import torch.nn as nn


class MultiHeadAttentionBlock(nn.Module):

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

        out, _ = self.attention(

            x,

            x,

            x

        )

        return out