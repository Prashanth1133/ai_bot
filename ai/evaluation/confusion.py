from sklearn.metrics import confusion_matrix


class Confusion:

    def compute(

        self,

        y_true,

        y_pred,

    ):

        return confusion_matrix(

            y_true,

            y_pred,

        )