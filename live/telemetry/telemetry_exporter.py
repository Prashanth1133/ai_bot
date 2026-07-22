import json
from pathlib import Path


class TelemetryExporter:

    @staticmethod
    def export(

        records,

        filename,

    ):

        output = []

        for record in records:

            output.append({

                "component": record.component,

                "metric": record.metric,

                "value": record.value,

                "unit": record.unit,

                "labels": record.labels,

                "timestamp": record.timestamp.isoformat(),

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