class SelfAnalyzer:

    def __init__(self):

        self.reports = []

    def add(
        self,
        report
    ):

        self.reports.append(
            report
        )

    def latest(self):

        if not self.reports:
            return {}

        return self.reports[-1]

    def evaluate(self):

        report = self.latest()

        return {
            "accuracy":
            report.get(
                "win_rate",
                0
            ),

            "trades":
            report.get(
                "trades",
                0
            ),

            "profit":
            report.get(
                "profit",
                0
            ),
        }