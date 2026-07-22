from __future__ import annotations

import pandas as pd


class HistoricalDataLoader:

    REQUIRED_COLUMNS = [

        "timestamp",

        "symbol",

        "open",

        "high",

        "low",

        "close",

        "volume",

    ]

    def load_csv(

        self,

        path,

    ):

        df = pd.read_csv(path)

        self.validate(df)

        return df

    def load_parquet(

        self,

        path,

    ):

        df = pd.read_parquet(path)

        self.validate(df)

        return df

    def validate(

        self,

        dataframe,

    ):

        missing = [

            c

            for c in self.REQUIRED_COLUMNS

            if c not in dataframe.columns

        ]

        if missing:

            raise ValueError(

                f"Missing columns: {missing}"

            )

        dataframe.sort_values(

            "timestamp",

            inplace=True,

        )

        dataframe.reset_index(

            drop=True,

            inplace=True,

        )