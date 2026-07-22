from __future__ import annotations

import time

from live.ai.model_cache import ModelCache
from live.ai.prediction_result import PredictionResult


class InferencePipeline:
    """
    Production inference pipeline.
    """

    def __init__(self):

        self.cache = ModelCache()

    ############################################################

    def predict(

        self,

        feature_vector,

    ) -> PredictionResult:

        model = self.cache.get()

        if model is None:

            raise RuntimeError(

                "No production model loaded."

            )

        prediction = model.predict(

            feature_vector

        )

        return PredictionResult(

            direction=prediction["direction"],

            confidence=float(

                prediction["confidence"]

            ),

            probabilities=prediction.get(

                "probabilities",

                [],

            ),

            timestamp=int(time.time() * 1000),

            model_version=prediction.get(

                "model_version",

                "unknown",

            ),

        )