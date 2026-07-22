import os

import torch
import torch.nn as nn

from torch.utils.data import DataLoader


class Trainer:

    def __init__(

        self,
        model,
        dataset,
        save_path="models/trading_transformer.pt",
        batch_size=64,
        lr=1e-4

    ):

        self.model = model

        self.save_path = save_path

        self.loader = DataLoader(

            dataset,

            batch_size=batch_size,

            shuffle=True

        )

        self.optimizer = torch.optim.AdamW(

            self.model.parameters(),

            lr=lr

        )

        self.ce = nn.CrossEntropyLoss()

        self.mse = nn.MSELoss()

    def train(

        self,
        epochs=20

    ):

        self.model.train()

        for epoch in range(epochs):

            total_loss = 0.0

            for x, y in self.loader:

                outputs = self.model(x)

                loss = 0

                loss += self.ce(
                    outputs["direction"],
                    y["direction"]
                )

                loss += self.ce(
                    outputs["reversal"],
                    y["reversal"]
                )

                loss += self.ce(
                    outputs["market_regime"],
                    y["market_regime"]
                )

                loss += self.mse(
                    outputs["confidence"].squeeze(),
                    y["confidence"]
                )

                loss += self.mse(
                    outputs["volatility"].squeeze(),
                    y["volatility"]
                )

                loss += self.mse(
                    outputs["take_profit"].squeeze(),
                    y["take_profit"]
                )

                loss += self.mse(
                    outputs["stop_loss"].squeeze(),
                    y["stop_loss"]
                )

                self.optimizer.zero_grad()

                loss.backward()

                torch.nn.utils.clip_grad_norm_(

                    self.model.parameters(),

                    1.0

                )

                self.optimizer.step()

                total_loss += loss.item()

            print(

                f"Epoch {epoch + 1}/{epochs} "
                f"Loss={total_loss:.4f}"

            )

        os.makedirs(

            "models",

            exist_ok=True

        )

        torch.save(

            self.model.state_dict(),

            self.save_path

        )

        print(

            f"\nModel Saved: {self.save_path}"

        )