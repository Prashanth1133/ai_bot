class PaperPortfolio:


    def __init__(self):

        self.balance = 10000

        self.profit = 0

        self.loss = 0

        self.positions = []


    def add_position(

        self,
        position

    ):


        self.positions.append(

            position

        )


    def add_profit(

        self,
        amount

    ):


        self.profit += amount

        self.balance += amount


    def add_loss(

        self,
        amount

    ):


        self.loss += amount

        self.balance -= amount


    def summary(self):


        print("\n")


        print(

            "Balance :",

            self.balance

        )


        print(

            "Profit :",

            self.profit

        )


        print(

            "Loss :",

            self.loss

        )


        print(

            "Positions :",

            len(

                self.positions

            )

        )


        print("\n")