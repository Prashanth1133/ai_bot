from __future__ import annotations

from datetime import datetime


class ModelHealth:

    def __init__(self):

        self.loaded = False

        self.last_prediction = None

        self.total_predictions = 0

        self.failed_predictions = 0

    ########################################################

    def model_loaded(self):

        self.loaded = True

    ########################################################

    def prediction_success(self):

        self.total_predictions += 1

        self.last_prediction = datetime.utcnow()

    ########################################################

    def prediction_failed(self):

        self.failed_predictions += 1

    ########################################################

    def status(self):

        return {

            "loaded": self.loaded,

            "last_prediction": self.last_prediction,

            "total_predictions": self.total_predictions,

            "failed_predictions": self.failed_predictions,

            "success_rate": (

                0.0

                if self.total_predictions == 0

                else (

                    (self.total_predictions - self.failed_predictions)

                    / self.total_predictions

                )

            ),

        }