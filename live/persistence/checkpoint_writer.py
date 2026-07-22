from __future__ import annotations

import json
from pathlib import Path


class CheckpointWriter:

    @staticmethod
    def write(
        checkpoint,
        filename: str,
    ):

        Path(filename).parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with open(
            filename,
            "w",
            encoding="utf-8",
        ) as fp:

            json.dump(
                {
                    "name": checkpoint.name,
                    "timestamp": checkpoint.timestamp.isoformat(),
                    "state": checkpoint.state,
                },
                fp,
                indent=4,
            )