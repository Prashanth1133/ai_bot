from __future__ import annotations

import json
from pathlib import Path


class FileLogHandler:

    def __init__(
        self,
        filename: str,
    ):

        self.path = Path(filename)

        self.path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

    async def __call__(
        self,
        record,
    ):

        with open(
            self.path,
            "a",
            encoding="utf-8",
        ) as fp:

            fp.write(
                json.dumps(
                    {
                        "timestamp": record.timestamp.isoformat(),
                        "level": record.level,
                        "component": record.component,
                        "message": record.message,
                        "metadata": record.metadata,
                    }
                )
                + "\n"
            )