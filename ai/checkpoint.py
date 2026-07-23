import os
import time

import torch


class CheckpointManager:

    def __init__(

        self,
        model,
        checkpoint_dir="checkpoints",
        interval=1800

    ):

        self.model = model

        self.interval = interval

        self.last_save = time.time()

        self.checkpoint_dir = checkpoint_dir

        os.makedirs(

            self.checkpoint_dir,

            exist_ok=True

        )

    def save(

        self,
        epoch=None,
        loss=None,
        force=False

    ):

        now = time.time()

        if (

            not force

            and

            (now - self.last_save)

            < self.interval

        ):

            return None


        filename = (

            f"checkpoint_"

            f"epoch_{epoch}_"

            f"{int(now)}.pt"

        )


        path = os.path.join(

            self.checkpoint_dir,

            filename

        )


        checkpoint = {

            "epoch": epoch,

            "loss": loss,

            "model_state_dict":

                self.model.state_dict()

        }


        torch.save(

            checkpoint,

            path

        )


        self.last_save = now


        print(

            f"\nCheckpoint Saved : "

            f"{path}"

        )


        return path


    def save_best(

        self,
        loss

    ):


        path = os.path.join(

            self.checkpoint_dir,

            "best_model.pt"

        )


        checkpoint = {

            "loss": loss,

            "model_state_dict":

                self.model.state_dict()

        }


        torch.save(

            checkpoint,

            path

        )


        print(

            "\nBest Model Updated : "

            f"{path}"

        )


        return path


    def load(

        self,
        path

    ):


        checkpoint = torch.load(

            path,

            map_location="cpu"

        )


        self.model.load_state_dict(

            checkpoint[

                "model_state_dict"

            ]

        )


        print(

            f"\nCheckpoint Loaded : "

            f"{path}"

        )


        return checkpoint