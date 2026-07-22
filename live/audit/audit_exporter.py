import json
from pathlib import Path


class AuditExporter:

    @staticmethod
    def export(events, filename):

        output = []

        for event in events:

            output.append({

                "id": event.event_id,

                "category": event.category,

                "action": event.action,

                "component": event.component,

                "user": event.user,

                "success": event.success,

                "message": event.message,

                "metadata": event.metadata,

                "timestamp": event.timestamp.isoformat(),

            })

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
                output,
                fp,
                indent=4,
            )