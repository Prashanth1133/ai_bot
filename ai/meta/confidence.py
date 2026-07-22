class ConfidenceEngine:

    def calculate(
        self,
        outputs
    ):

        total = (
            sum(
                outputs
            )
        )

        return max(
            outputs
        ) / total