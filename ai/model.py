# ai/model.py

import torch
import torch.nn as nn

from ai.embeddings import FeatureEmbedding
from ai.positional_encoding import PositionalEncoding
from ai.transformer_block import TransformerBlock
from ai.pooling import AttentionPooling
from ai.heads import MultiTaskHeads


class TradingTransformer(nn.Module):
    """
    Institutional Multi-Task Transformer Model

    Outputs:
        - direction (3 classes: SELL=0, HOLD=1, BUY=2)
        - signal_logits
        - reversal
        - return_15m
        - return_1h
        - return_4h
        - max_return_1h
        - min_return_1h
        - take_profit
        - stop_loss
        - attention
        - embedding
    """

    def __init__(
        self,
        input_dim: int = 48,
        d_model: int = 256,
        heads: int = 8,
        layers: int = 6,
        dropout: float = 0.10,
    ):
        super().__init__()

        self.input_dim = input_dim
        self.d_model = d_model

        # --------------------------------------------------
        # Input Embedding
        # --------------------------------------------------
        self.embedding = FeatureEmbedding(
            input_dim=input_dim,
            d_model=d_model,
        )

        # --------------------------------------------------
        # Positional Encoding
        # --------------------------------------------------
        self.position = PositionalEncoding(
            d_model=d_model
        )

        # --------------------------------------------------
        # Transformer Encoder Stack
        # --------------------------------------------------
        self.blocks = nn.ModuleList(
            [
                TransformerBlock(
                    d_model=d_model,
                    heads=heads,
                    dropout=dropout,
                )
                for _ in range(layers)
            ]
        )

        # --------------------------------------------------
        # Global Attention Pooling
        # --------------------------------------------------
        self.pool = AttentionPooling(
            d_model=d_model
        )

        # --------------------------------------------------
        # Multi Task Prediction Heads
        # --------------------------------------------------
        self.heads = MultiTaskHeads(
            d_model=d_model
        )

        # --------------------------------------------------
        # Optional latent representation
        # --------------------------------------------------
        self.latent = nn.Sequential(
            nn.Linear(d_model, d_model),
            nn.GELU(),
            nn.Dropout(dropout),
        )

    def encode(self, x):
        """
        Produces latent representation only.
        """

        x = self.embedding(x)
        x = self.position(x)

        attention_maps = []

        for block in self.blocks:
            x, attn = block(x)
            attention_maps.append(attn)

        pooled = self.pool(x)
        latent = self.latent(pooled)

        return latent, attention_maps

    def forward(self, x):
        """
        Parameters
        ----------
        x:
            Shape:
                [batch, sequence, features]

        Returns
        -------
        dict
        """

        latent, attention_maps = self.encode(x)

        outputs = self.heads(latent)

        outputs["attention"] = attention_maps
        outputs["embedding"] = latent

        return outputs

    @torch.no_grad()
    def predict(self, x):
        """
        Inference helper.
        """

        self.eval()

        outputs = self.forward(x)

        logits = outputs.get("signal_logits", outputs.get("direction"))
        if logits is not None:

            probs = torch.softmax(
                logits,
                dim=-1,
            )

            confidence, signal = torch.max(
                probs,
                dim=-1,
            )

            outputs["signal"] = signal
            outputs["confidence_score"] = confidence

        return outputs

    def num_parameters(self):
        """
        Total trainable parameters.
        """

        return sum(
            p.numel()
            for p in self.parameters()
            if p.requires_grad
        )


if __name__ == "__main__":

    model = TradingTransformer(
        input_dim=400,
        d_model=256,
        heads=8,
        layers=6,
        dropout=0.10,
    )

    x = torch.randn(
        4,      # batch
        128,    # sequence length
        400,    # features
    )

    outputs = model(x)

    print("\nMODEL OUTPUTS")
    print("=" * 50)

    for key, value in outputs.items():

        if isinstance(value, list):

            print(
                f"{key:<20}: "
                f"{len(value)} attention maps"
            )

        elif torch.is_tensor(value):

            print(
                f"{key:<20}: "
                f"{tuple(value.shape)}"
            )

        else:

            print(
                f"{key:<20}: "
                f"{type(value).__name__}"
            )

    print("\nParameters:")
    print(
        f"{model.num_parameters():,}"
    )