import os
import time

import torch


class CheckpointManager:

    def __init__(

        self,
        model,
        interval=3600

    ):

        self.model = model

        self.interval = interval

        self.last_save = time.time()

        os.makedirs(

            "models/checkpoints",

            exist_ok=True

        )

    def save(

        self,
        force=False

    ):

        now = time.time()

        if (

            now - self.last_save
            < self.interval

            and

            not force

        ):

            return

        filename = (

            f"models/checkpoints/"
            f"checkpoint_"
            f"{int(now)}.pt"

        )

        torch.save(

            self.model.state_dict(),

            filename

        )

        self.last_save = now

        print(

            f"Checkpoint: {filename}"

        )