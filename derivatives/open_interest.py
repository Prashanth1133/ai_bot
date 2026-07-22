class OpenInterestAnalyzer:

    def analyze(

        self,

        oi_previous,

        oi_current

    ):

        if oi_current > oi_previous:

            return "INCREASING"

        if oi_current < oi_previous:

            return "DECREASING"

        return "UNCHANGED"