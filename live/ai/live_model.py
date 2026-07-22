from __future__ import annotations

from decimal import Decimal
from typing import Any

from app.logger import logger


class LiveModel:
    """
    Loads the production AI model and performs inference.

    This class is the only component that should directly
    communicate with the trained model during live trading.
    """

    def __init__(self, predictor):

        self.predictor = predictor

        self.model_loaded = False

    ###############################################################

    def load(self):

        """
        Load latest production model.
        """

        self.predictor.load_latest()

        self.model_loaded = True

        logger.success("Live AI model loaded.")

    ###############################################################

    def predict(
        self,
        feature_vector,
    ):

        if not self.model_loaded:
            self.load()

        return self.predictor.predict(feature_vector)

    ###############################################################

    def confidence(
        self,
        feature_vector,
    ) -> Decimal:

        prediction = self.predict(feature_vector)

        if isinstance(prediction, dict):

            return Decimal(
                str(
                    prediction.get(
                        "confidence",
                        0,
                    )
                )
            )

        return Decimal("0")

    ###############################################################

    def direction(
        self,
        feature_vector,
    ):

        prediction = self.predict(feature_vector)

        if isinstance(prediction, dict):

            return prediction.get(
                "direction",
                "HOLD",
            )

        return "HOLD"

    ###############################################################

    def probabilities(
        self,
        feature_vector,
    ):

        prediction = self.predict(feature_vector)

        if isinstance(prediction, dict):

            return prediction.get(
                "probabilities",
                {},
            )

        return {}

    ###############################################################

    def raw(
        self,
        feature_vector,
    ) -> Any:

        return self.predict(feature_vector)