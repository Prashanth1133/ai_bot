from __future__ import annotations

import pandas as pd


class TimeframeSynchronizer:

    @staticmethod
    def synchronize(

        *frames,

    ):

        if not frames:

            return []

        base = frames[0].index

        aligned = []

        for frame in frames:

            aligned.append(

                frame.reindex(

                    base,

                    method="ffill",

                )

            )

        return aligned