from decimal import Decimal


class PortfolioManager:


    def __init__(self):


        self.balance = Decimal(

            "10000"

        )

        self.total_profit = Decimal(

            "0"

        )

        self.total_loss = Decimal(

            "0"

        )

        self.total_trades = 0


    def update_profit(

        self,
        amount

    ):


        amount = Decimal(

            str(amount)

        )


        self.total_profit += amount

        self.balance += amount

        self.total_trades += 1


    def update_loss(

        self,
        amount

    ):


        amount = Decimal(

            str(amount)

        )


        self.total_loss += amount

        self.balance -= amount

        self.total_trades += 1


    def summary(self):


        print("\n")


        print(

            "Balance :",

            self.balance

        )


        print(

            "Profit :",

            self.total_profit

        )


        print(

            "Loss :",

            self.total_loss

        )


        print(

            "Trades :",

            self.total_trades

        )


        print("\n")