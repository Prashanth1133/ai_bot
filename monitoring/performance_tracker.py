import time


class PerformanceTracker:

    def __init__(self):

        self.total = 0
        self.wins = 0
        self.losses = 0

        self.started = time.time()

    def record(

        self,
        pnl

    ):

        self.total += 1

        if pnl > 0:

            self.wins += 1

        else:

            self.losses += 1

    def statistics(self):

        win_rate = 0

        if self.total:

            win_rate = (

                self.wins /
                self.total

            )

        return {

            "trades":

                self.total,

            "wins":

                self.wins,

            "losses":

                self.losses,

            "win_rate":

                round(

                    win_rate,

                    4

                ),

            "uptime":

                int(

                    time.time()

                    -

                    self.started

                )

        }