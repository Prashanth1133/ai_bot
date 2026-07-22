from __future__ import annotations

import pandas as pd


class ParquetWriter:

    @staticmethod
    def write(

        dataframe,

        filename,

    ):

        if not isinstance(

            dataframe,

            pd.DataFrame,

        ):

            dataframe = pd.DataFrame(

                dataframe

            )

        dataframe.to_parquet(

            filename,

            index=False,

        )