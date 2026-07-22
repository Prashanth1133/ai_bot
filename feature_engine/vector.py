from dataclasses import dataclass

import numpy as np

from feature_engine.feature_names import FEATURES


@dataclass(slots=True)
class FeatureVector:

    symbol: str

    timeframe: str

    timestamp: int

    values: np.ndarray


class FeatureVectorBuilder:

    def build(

        self,

        symbol,

        timeframe,

        timestamp,

        feature_store

    ):

        values = []

        for feature in FEATURES:

            values.append(

                float(

                    feature_store.get(

                        feature,

                        0

                    )

                )

            )

        return FeatureVector(

            symbol,

            timeframe,

            timestamp,

            np.asarray(

                values,

                dtype=np.float32

            )

        )