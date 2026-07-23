import pandas as pd


class MultiTimeFrameBuilder:

    def __init__(self):

        self.timeframes = [

            "1min",
            "5min",
            "15min",
            "30min",
            "1h",
            "4h",
            "1d"

        ]

    def build(

        self,
        dataframe

    ):

        datasets = {}

        for timeframe in self.timeframes:

            datasets[timeframe] = (

                self.resample(

                    dataframe,
                    timeframe

                )

            )

        return datasets

    def resample(

        self,
        dataframe,
        timeframe

    ):

        df = dataframe.copy()

        if "time" in df.columns:

            df["time"] = pd.to_datetime(

                df["time"]

            )

            df = df.set_index(

                "time"

            )

        candles = (

            df.resample(

                timeframe

            )

            .agg(

                {

                    "open": "first",

                    "high": "max",

                    "low": "min",

                    "close": "last",

                    "volume": "sum"

                }

            )

            .dropna()

        )

        return candles.reset_index()