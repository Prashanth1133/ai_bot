class ConfidenceFilter:

    def __init__(
        self,
        threshold: float = 0.65,
    ):
        self.threshold = threshold

    def allow(
        self,
        prediction,
    ):

        return (
            prediction.confidence
            >= self.threshold
        )