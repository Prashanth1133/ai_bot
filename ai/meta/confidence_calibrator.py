class ConfidenceCalibrator:

    """
    Adjusts AI confidence according
    to recent performance.
    """

    def calibrate(

        self,

        confidence,

        win_rate,

    ):

        if win_rate < 0.40:

            confidence *= 0.80

        elif win_rate > 0.70:

            confidence *= 1.10

        return min(confidence, 1.0)