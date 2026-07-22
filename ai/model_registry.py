from pathlib import Path

import torch


class ModelRegistry:

    def __init__(self):

        self.path = Path(
            "artifacts/models"
        )

        self.path.mkdir(
            parents=True,
            exist_ok=True
        )

    def save(
        self,
        model,
        name
    ):

        file = self.path / f"{name}.pt"

        torch.save(
            model.state_dict(),
            file
        )

        return str(file)

    def load(
        self,
        model,
        name
    ):

        file = self.path / f"{name}.pt"

        model.load_state_dict(
            torch.load(
                file,
                map_location="cpu"
            )
        )

        return model