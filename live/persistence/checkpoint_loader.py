from __future__ import annotations

import json

from live.persistence.checkpoint import Checkpoint


class CheckpointLoader:

    @staticmethod
    def load(
        filename: str,
    ):

        with open(
            filename,
            "r",
            encoding="utf-8",
        ) as fp:

            data = json.load(fp)

        return Checkpoint(
            name=data["name"],
            state=data["state"],
        )