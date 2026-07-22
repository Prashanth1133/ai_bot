from __future__ import annotations

import json
from pathlib import Path


class ConfigWriter:

    @staticmethod
    def write(
        path: str,
        config: dict,
    ):

        with open(
            Path(path),
            "w",
            encoding="utf-8",
        ) as fp:

            json.dump(
                config,
                fp,
                indent=4,
            )