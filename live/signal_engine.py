from __future__ import annotations

from live.inference_engine import LiveInferenceEngine


class LiveSignalEngine:

    def __init__(

        self,

        model,

        confidence_threshold=0.75,

    ):

        self.ai = LiveInferenceEngine(model)

        self.threshold = confidence_threshold

    ##########################################################

    def evaluate(

        self,

        feature_vector,

    ):

        result = self.ai.predict(

            feature_vector

        )

        if result["confidence"] < self.threshold:

            return None

        signal = "BUY"

        if result["prediction"] == 0:

            signal = "SELL"

        return {

            "signal": signal,

            "confidence": result["confidence"],

            "probabilities": result["probabilities"],

        }