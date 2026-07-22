class PatternDetector:

    def detect(
        self,
        closes
    ):

        if (
            closes[-1]
            > max(
                closes[-5:-1]
            )
        ):

            return "BREAKOUT"

        if (
            closes[-1]
            < min(
                closes[-5:-1]
            )
        ):

            return "BREAKDOWN"

        return "NONE"