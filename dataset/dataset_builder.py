from __future__ import annotations

import pandas as pd


class DatasetBuilder:

    def build(

        self,

        features,

        labels,

    ):

        frame = pd.DataFrame(

            features

        )

        frame["label"] = labels

        return frame