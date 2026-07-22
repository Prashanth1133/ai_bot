from sklearn.calibration import calibration_curve


class ConfidenceCalibration:

    def evaluate(

        self,

        y_true,

        probabilities,

    ):

        return calibration_curve(

            y_true,

            probabilities,

            n_bins=10,

        )