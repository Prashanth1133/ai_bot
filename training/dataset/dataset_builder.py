from __future__ import annotations

import pandas as pd


class DatasetBuilder:
    """
    Builds the final ML dataset from
    engineered features.
    """

    def __init__(self):

        self.frames = []

    ########################################################

    def add_features(

        self,

        dataframe: pd.DataFrame,

    ):

        self.frames.append(dataframe)

    ########################################################

    def build(self):

        if not self.frames:

            raise RuntimeError(
                "No feature data available."
            )

        dataset = pd.concat(

            self.frames,

            ignore_index=True,

        )

        dataset = dataset.dropna()

        dataset = dataset.reset_index(

            drop=True

        )

        return dataset