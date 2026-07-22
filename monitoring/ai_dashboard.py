class AIDashboard:

    def __init__(

        self,
        tracker

    ):

        self.tracker = tracker

    def display(self):

        stats = (

            self.tracker

            .statistics()

        )

        print()

        print("=" * 60)

        print(

            "AI DASHBOARD"

        )

        print("=" * 60)

        print(

            f"Trades    : "
            f"{stats['trades']}"
        )

        print(

            f"Wins      : "
            f"{stats['wins']}"
        )

        print(

            f"Losses    : "
            f"{stats['losses']}"
        )

        print(

            f"Win Rate  : "
            f"{stats['win_rate']:.2%}"
        )

        print(

            f"Uptime    : "
            f"{stats['uptime']} sec"
        )

        print("=" * 60)