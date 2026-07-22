from sklearn.metrics import (
    precision_score,
    recall_score,
    f1_score,
    accuracy_score,
)


class ClassificationMetrics:

    def evaluate(

        self,

        y_true,

        y_pred,

    ):

        return {

            "accuracy": accuracy_score(

                y_true,

                y_pred,

            ),

            "precision": precision_score(

                y_true,

                y_pred,

                average="macro",

                zero_division=0,

            ),

            "recall": recall_score(

                y_true,

                y_pred,

                average="macro",

                zero_division=0,

            ),

            "f1": f1_score(

                y_true,

                y_pred,

                average="macro",

                zero_division=0,

            ),

        }