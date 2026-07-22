from __future__ import annotations

import json
from pathlib import Path


class MetricsExporter:

    @staticmethod
    def export(
        manager,
        filename: str,
    ):

        output = {

            "counters": {
                k: v.get()
                for k, v in manager.counters.items()
            },

            "gauges": {
                k: v.get()
                for k, v in manager.gauges.items()
            },

            "histograms": {
                k: {
                    "count": v.count(),
                    "average": v.average(),
                    "min": v.minimum(),
                    "max": v.maximum(),
                }
                for k, v in manager.histograms.items()
            },
        }

        with open(
            Path(filename),
            "w",
            encoding="utf-8",
        ) as fp:

            json.dump(
                output,
                fp,
                indent=4,
            )