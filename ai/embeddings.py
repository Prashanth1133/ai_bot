import torch.nn as nn


class FeatureEmbedding(nn.Module):

    """
    Converts raw market features into the
    transformer latent dimension.
    """

    def __init__(
        self,
        input_dim: int,
        d_model: int
    ):

        super().__init__()

        self.network = nn.Sequential(

            nn.Linear(
                input_dim,
                d_model
            ),

            nn.LayerNorm(
                d_model
            ),

            nn.GELU(),

            nn.Dropout(
                0.1
            ),

            nn.Linear(
                d_model,
                d_model
            ),

            nn.LayerNorm(
                d_model
            )

        )

    def forward(self, x):

        return self.network(x)