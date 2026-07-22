import torch.nn as nn

from ai.attention import MultiHeadSelfAttention


class TransformerBlock(nn.Module):

    def __init__(
        self,
        d_model,
        heads,
        dropout=0.1
    ):

        super().__init__()

        self.attention = MultiHeadSelfAttention(
            d_model,
            heads
        )

        self.norm1 = nn.LayerNorm(
            d_model
        )

        self.norm2 = nn.LayerNorm(
            d_model
        )

        self.ff = nn.Sequential(

            nn.Linear(
                d_model,
                d_model * 4
            ),

            nn.GELU(),

            nn.Dropout(
                dropout
            ),

            nn.Linear(
                d_model * 4,
                d_model
            ),

            nn.Dropout(
                dropout
            )

        )

    def forward(self, x):

        attn_output, weights = self.attention(
            x
        )

        x = self.norm1(
            x + attn_output
        )

        ff = self.ff(
            x
        )

        x = self.norm2(
            x + ff
        )

        return x, weights