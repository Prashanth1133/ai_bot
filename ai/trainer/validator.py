from sklearn.metrics import (
    accuracy_score,
    f1_score
)


class Validator:

    def evaluate(
        self,
        y_true,
        y_pred
    ):

        return {

            "accuracy":
            accuracy_score(
                y_true,
                y_pred
            ),

            "f1":
            f1_score(
                y_true,
                y_pred,
                average="macro"
            ),
        }