from __future__ import annotations

import json
from pathlib import Path


class ConfigLoader:

    @staticmethod
    def load(path: str):

        with open(
            Path(path),
            "r",
            encoding="utf-8",
        ) as fp:

            return json.load(fp)