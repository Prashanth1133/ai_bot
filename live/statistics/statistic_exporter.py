import json
from pathlib import Path


class StatisticExporter:

    @staticmethod
    def export(

        statistics,

        filename,

    ):

        output = []

        for statistic in statistics:

            output.append({

                "name": statistic.name,

                "value": statistic.value,

                "unit": statistic.unit,

                "metadata": statistic.metadata,

                "updated_at": statistic.updated_at.isoformat(),

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