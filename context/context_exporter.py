import json
from dataclasses import asdict


class ContextExporter:

    @staticmethod
    def export(

        snapshot,

        filename,

    ):

        with open(

            filename,

            "w",

            encoding="utf-8",

        ) as fp:

            json.dump(

                asdict(snapshot),

                fp,

                indent=4,

                default=str,

            )