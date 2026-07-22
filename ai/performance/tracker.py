class PerformanceTracker:

    def __init__(self):

        self.data = []

    def add(
        self,
        trade
    ):

        self.data.append(
            trade
        )

    def report(self):

        wins = len(
            [
                x
                for x
                in self.data
                if x > 0
            ]
        )

        total = len(
            self.data
        )

        return {

            "trades":
            total,

            "wins":
            wins,

            "win_rate":
            (
                wins /
                max(
                    total,
                    1
                )
            ) * 100,

            "profit":
            sum(
                self.data
            ),
        }