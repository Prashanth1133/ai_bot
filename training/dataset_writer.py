from __future__ import annotations

from pathlib import Path

import pandas as pd


class DatasetWriter:
    """
    Saves processed datasets.
    """

    def __init__(

        self,

        output_folder="datasets",

    ):

        self.output = Path(output_folder)

        self.output.mkdir(

            parents=True,

            exist_ok=True,

        )

    ########################################################

    def write_csv(

        self,

        dataframe: pd.DataFrame,

        filename: str,

    ):

        path = self.output / f"{filename}.csv"

        dataframe.to_csv(

            path,

            index=False,

        )

        return path

    ########################################################

    def write_parquet(

        self,

        dataframe: pd.DataFrame,

        filename: str,

    ):

        path = self.output / f"{filename}.parquet"

        dataframe.to_parquet(

            path,

            index=False,

        )

        return path

    ########################################################

    def write(

        self,

        dataframe: pd.DataFrame,

        filename: str,

        format="parquet",

    ):

        if format == "csv":

            return self.write_csv(

                dataframe,

                filename,

            )

        return self.write_parquet(

            dataframe,

            filename,

        )