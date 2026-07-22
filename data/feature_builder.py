import numpy as np
import pandas as pd


class FeatureBuilder:

    def build(self, df):

        df = df.copy()

        df["returns"] = df["close"].pct_change()

        df["ema_10"] = (

            df["close"]

            .ewm(span=10)

            .mean()

        )

        df["ema_50"] = (

            df["close"]

            .ewm(span=50)

            .mean()

        )

        df["volatility"] = (

            df["returns"]

            .rolling(20)

            .std()

        )

        df["volume_mean"] = (

            df["volume"]

            .rolling(20)

            .mean()

        )

        df["high_low"] = (

            df["high"]

            - df["low"]

        )

        df["open_close"] = (

            df["close"]

            - df["open"]

        )

        df["rsi"] = self.rsi(

            df["close"]

        )

        df = df.dropna()

        features = df[

            [

                "open",
                "high",
                "low",
                "close",
                "volume",
                "returns",
                "ema_10",
                "ema_50",
                "volatility",
                "volume_mean",
                "rsi"

            ]

        ].values

        return features

    def rsi(

        self,
        series,
        period=14

    ):

        delta = series.diff()

        gain = delta.clip(

            lower=0

        )

        loss = -delta.clip(

            upper=0

        )

        avg_gain = gain.rolling(

            period

        ).mean()

        avg_loss = loss.rolling(

            period

        ).mean()

        rs = avg_gain / (

            avg_loss + 1e-8

        )

        return (

            100 -

            (100 / (1 + rs))

        )