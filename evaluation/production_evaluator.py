import numpy as np


class ProductionEvaluator:


    def accuracy(

        self,
        predictions,
        labels

    ):


        predictions = np.array(

            predictions

        )

        labels = np.array(

            labels

        )


        return float(

            (

                predictions == labels

            ).mean()

        )


    def mean_error(

        self,
        predictions,
        labels

    ):


        predictions = np.array(

            predictions

        )

        labels = np.array(

            labels

        )


        return float(

            np.mean(

                np.abs(

                    predictions-labels

                )

            )

        )


    def confidence_score(

        self,
        confidence

    ):


        return float(

            np.mean(

                confidence

            )

        )


    def evaluate(

        self,
        predictions,
        labels=None,
        confidence=None,

    ):


        # Support historical report dictionaries while retaining the explicit
        # prediction/label API used by the production evaluator.
        if isinstance(predictions, dict) and labels is None and confidence is None:
            return dict(predictions)

        if labels is None or confidence is None:
            raise ValueError("labels and confidence are required for prediction evaluation")

        return {

            "accuracy":

            self.accuracy(

                predictions,
                labels

            ),

            "mean_error":

            self.mean_error(

                predictions,
                labels

            ),

            "confidence":

            self.confidence_score(

                confidence

            )

        }
