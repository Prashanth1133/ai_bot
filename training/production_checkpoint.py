import os
import torch


class ProductionCheckpoint:

    def __init__(self):

        os.makedirs(

            "models/checkpoints",

            exist_ok=True

        )

    def save(

        self,
        model,
        epoch=None,
        filename=None

    ):

        if filename is not None:

            path = os.path.join(

                "models",
                filename

            )

        elif epoch is not None:

            path = os.path.join(

                "models/checkpoints",

                f"production_epoch_{epoch}.pt"

            )

        else:

            path = os.path.join(

                "models",

                "production_v1.pt"

            )

        torch.save(

            model.state_dict(),

            path

        )

        print(

            f"\nModel Saved : {path}"

        )

        return path