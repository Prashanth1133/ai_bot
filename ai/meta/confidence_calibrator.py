class ConfidenceCalibrator:

    """
    Preserve raw model confidence.

    Calibration should only be enabled after
    a validated calibration procedure.
    """

    def calibrate(
        self,
        confidence,
        win_rate,
    ):

        if win_rate is None:

            return float(confidence)

        return float(confidence)