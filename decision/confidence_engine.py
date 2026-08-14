class ConfidenceEngine:

    """
    Preserve the AI model's confidence.

    A separate ensemble should only modify confidence
    when multiple independently validated models exist.
    """

    def calculate(self, signal):

        confidence = getattr(
            signal,
            "confidence",
            None,
        )

        if confidence is None:

            return 0.0

        return float(confidence)