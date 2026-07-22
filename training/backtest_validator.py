class BacktestValidator:

    """
    Compares AI predictions against
    historical outcomes.
    """

    def validate(

        self,

        predictions,

        labels,

    ):

        correct = (

            predictions == labels

        ).sum()

        return correct / len(labels)