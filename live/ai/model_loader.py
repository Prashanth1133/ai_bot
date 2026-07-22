from __future__ import annotations

from pathlib import Path

import torch

from app.logger import logger


class LiveModelLoader:
    """
    Loads trained production models.
    """

    def __init__(

        self,

        model_directory="storage/models",

        device=None,

    ):

        self.model_directory = Path(

            model_directory

        )

        self.device = device or (

            "cuda"

            if torch.cuda.is_available()

            else "cpu"

        )

    ############################################################

    def latest_model(self):

        models = sorted(

            self.model_directory.glob("*.pt"),

            key=lambda p: p.stat().st_mtime,

            reverse=True,

        )

        if not models:

            raise FileNotFoundError(

                "No trained model found."

            )

        return models[0]

    ############################################################

    def load(

        self,

        model,

    ):

        path = self.latest_model()

        logger.info(

            f"Loading model {path.name}"

        )

        checkpoint = torch.load(

            path,

            map_location=self.device,

        )

        if isinstance(

            checkpoint,

            dict,

        ) and "state_dict" in checkpoint:

            model.load_state_dict(

                checkpoint["state_dict"]

            )

        else:

            model.load_state_dict(

                checkpoint

            )

        model.to(

            self.device

        )

        model.eval()

        logger.success(

            "Production model loaded."

        )

        return model

    ############################################################

    def device_name(self):

        return self.device