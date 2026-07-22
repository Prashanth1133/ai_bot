from __future__ import annotations

import pandas as pd


class TargetGenerator:
    """
    Generates BUY / SELL / HOLD labels
    from future returns.
    """

    def __init__(

        self,

        lookahead=20,

        threshold=0.003,

    ):

        self.lookahead = lookahead

        self.threshold = threshold

    ########################################################

    def generate(

        self,

        dataframe: pd.DataFrame,

    ):

        future = dataframe["close"].shift(

            -self.lookahead

        )

        returns = (

            future

            - dataframe["close"]

        ) / dataframe["close"]

        labels = []

        for r in returns:

            if pd.isna(r):

                labels.append(None)

            elif r > self.threshold:

                labels.append(1)

            elif r < -self.threshold:

                labels.append(-1)

            else:

                labels.append(0)

        dataframe["target"] = labels

        dataframe = dataframe.dropna()

        return dataframe