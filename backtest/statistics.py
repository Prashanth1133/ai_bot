class Statistics:


    def __init__(self):

        self.wins = 0

        self.losses = 0


    def add_win(self):

        self.wins += 1


    def add_loss(self):

        self.losses += 1


    def win_rate(self):


        total = (

            self.wins+

            self.losses

        )


        if total == 0:

            return 0


        return (

            self.wins/

            total

        )*100


    def summary(self):


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