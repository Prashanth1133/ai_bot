from __future__ import annotations

import pandas as pd


class CandleResampler:

    @staticmethod
    def resample(

        dataframe: pd.DataFrame,

        timeframe: str,

    ):

        return dataframe.resample(

            timeframe,

        ).agg(

            {

                "open": "first",

                "high": "max",

                "low": "min",

                "close": "last",

                "volume": "sum",

            }

        ).dropna()