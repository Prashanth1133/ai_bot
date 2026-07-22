from __future__ import annotations

from pathlib import Path
from datetime import datetime
from typing import Optional


class LiveModelRegistry:
    """
    Production model registry.
    """

    def __init__(

        self,

        model_directory="storage/models",

    ):

        self.model_directory = Path(model_directory)

        self.model_directory.mkdir(

            parents=True,

            exist_ok=True,

        )

    ############################################################

    def list_models(self):

        models = []

        for file in self.model_directory.glob("*"):

            if file.is_file():

                models.append(file)

        return sorted(

            models,

            key=lambda x: x.stat().st_mtime,

            reverse=True,

        )

    ############################################################

    def latest(self):

        models = self.list_models()

        if not models:

            return None

        return models[0]

    ############################################################

    def exists(self):

        return self.latest() is not None

    ############################################################

    def register(

        self,

        model_path,

    ):

        return Path(model_path)

    ############################################################

    def info(self):

        model = self.latest()

        if model is None:

            return None

        stat = model.stat()

        return {

            "name": model.name,

            "path": str(model),

            "size": stat.st_size,

            "modified": datetime.fromtimestamp(

                stat.st_mtime

            ),

        }

    ############################################################

    def load_path(self) -> Optional[str]:

        model = self.latest()

        if model is None:

            return None

        return str(model)