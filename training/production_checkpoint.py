import os
import torch


class ProductionCheckpoint:

    def __init__(self):
        os.makedirs(
            "models/Production/BTCUSDT/final_v1",
            exist_ok=True,
        )

    def save(
        self,
        model,
        epoch=None,
        filename=None,
    ):
        if filename is not None:
            if os.path.isabs(filename) or "/" in filename or "\\" in filename:
                path = filename
            else:
                path = os.path.join("models/Production/BTCUSDT/final_v1", filename)
        elif epoch is not None:
            path = os.path.join(
                "models/Production/BTCUSDT/final_v1/Epochs",
                f"epoch_{epoch}.pt",
            )
        else:
            path = os.path.join(
                "models/Production/BTCUSDT/final_v1",
                "final_model.pt",
            )

        os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)

        torch.save(
            model.state_dict(),
            path,
        )

        print(
            f"\nModel Saved : {path}"
        )

        return path