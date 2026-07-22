import pandas as pd

from ai.dataset.labels import create_label


class DatasetBuilder:

    def __init__(self, lookahead=5):
        self.lookahead = lookahead

    def build(self, file_path):

        df = pd.read_parquet(file_path)

        numeric = [
            "open",
            "high",
            "low",
            "close",
            "volume",
        ]

        for col in numeric:
            df[col] = df[col].astype(float)

        df["return_1"] = (
            df["close"].pct_change(1)
        )

        df["return_5"] = (
            df["close"].pct_change(5)
        )

        df["return_15"] = (
            df["close"].pct_change(15)
        )

        df["volume_ma"] = (
            df["volume"]
            .rolling(20)
            .mean()
        )

        df["volume_ratio"] = (
            df["volume"] /
            df["volume_ma"]
        )

        df["volatility"] = (
            df["close"]
            .rolling(20)
            .std()
        )

        df["future"] = (
            df["close"]
            .shift(-self.lookahead)
        )

        df["label"] = df.apply(
            lambda row:
            create_label(
                row["close"],
                row["future"]
            ),
            axis=1
        )

        df = df.dropna()

        features = [
            "return_1",
            "return_5",
            "return_15",
            "volume_ratio",
            "volatility",
        ]

        X = df[features]

        y = df["label"]

        return X, y, df