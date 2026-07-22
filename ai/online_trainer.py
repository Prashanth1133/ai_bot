import torch
import torch.nn as nn


class OnlineTrainer:

    def __init__(

        self,
        model,
        experience_buffer

    ):

        self.model = model

        self.buffer = experience_buffer

        self.optimizer = torch.optim.AdamW(

            model.parameters(),

            lr=1e-5

        )

        self.loss = nn.CrossEntropyLoss()

    def train_step(

        self,
        batch_size=64

    ):

        if len(

            self.buffer

        ) < batch_size:

            return

        batch = self.buffer.sample(

            batch_size

        )

        states = []
        labels = []

        for item in batch:

            states.append(
                item["state"]
            )

            labels.append(
                item["action"]
            )

        states = torch.stack(
            states
        )

        labels = torch.tensor(
            labels
        )

        outputs = self.model(
            states
        )

        loss = self.loss(

            outputs["direction"],

            labels

        )

        self.optimizer.zero_grad()

        loss.backward()

        self.optimizer.step()

        return float(
            loss.item()
        )