from __future__ import annotations

from pathlib import Path


class ModelWatcher:
    """
    Detects newly trained models.
    """

    def __init__(

        self,

        directory="storage/models",

    ):

        self.directory = Path(directory)

        self.last_timestamp = 0

    ###########################################################

    def changed(self):

        latest = self.latest()

        if latest is None:

            return False

        timestamp = latest.stat().st_mtime

        if timestamp > self.last_timestamp:

            self.last_timestamp = timestamp

            return True

        return False

    ###########################################################

    def latest(self):

        models = sorted(

            self.directory.glob("*.pt"),

            key=lambda x: x.stat().st_mtime,

            reverse=True,

        )

        if not models:

            return None

        return models[0]