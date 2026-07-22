from __future__ import annotations

import json
from pathlib import Path


class AuditWriter:

    @staticmethod
    def write(
        filename: str,
        records,
    ):

        Path(filename).parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        output = []

        for record in records:

            output.append(

                {

                    "audit_id": record.audit_id,

                    "component": record.component,

                    "action": record.action,

                    "user": record.user,

                    "payload": record.payload,

                    "timestamp": record.timestamp.isoformat(),

                }

            )

        with open(
            filename,
            "w",
            encoding="utf-8",
        ) as fp:

            json.dump(
                output,
                fp,
                indent=4,
            )