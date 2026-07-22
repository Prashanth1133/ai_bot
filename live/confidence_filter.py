class ConfidenceFilter:

    def __init__(

        self,

        threshold=0.85,

    ):

        self.threshold = threshold

    def allow(

        self,

        prediction,

    ):

        probability = prediction[
            "probability"
        ].max().item()

        return probability >= self.threshold