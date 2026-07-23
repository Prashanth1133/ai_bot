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
        labels,
        confidence

    ):


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