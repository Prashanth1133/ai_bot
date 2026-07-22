class PaperReport:

    def generate(
        self,
        trades
    ):

        wins = len(
            [
                x
                for x
                in trades
                if x > 0
            ]
        )

        return {

            "total":
            len(trades),

            "wins":
            wins,

            "losses":
            len(
                trades
            ) - wins,

            "profit":
            sum(
                trades
            )
        }