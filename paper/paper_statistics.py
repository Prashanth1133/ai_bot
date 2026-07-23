class PaperStatistics:


    def __init__(self):

        self.wins = 0

        self.losses = 0


    def add_win(self):

        self.wins += 1


    def add_loss(self):

        self.losses += 1


    def total(self):

        return (

            self.wins +

            self.losses

        )


    def win_rate(self):


        total = self.total()


        if total == 0:

            return 0


        return (

            self.wins/

            total

        ) * 100


    def summary(self):


        print("\n")


        print(

            "Wins :",

            self.wins

        )


        print(

            "Losses :",

            self.losses

        )


        print(

            "Win Rate :",

            round(

                self.win_rate(),

                2

            ),

            "%"

        )


        print("\n")