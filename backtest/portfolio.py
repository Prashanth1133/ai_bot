from decimal import Decimal


class BacktestPortfolio:


    def __init__(

        self,
        balance=Decimal("10000")

    ):

        self.balance = balance

        self.equity = balance

        self.positions = {}

        self.orders = []

        self.total_profit = Decimal("0")

        self.total_loss = Decimal("0")


    def add_profit(

        self,
        amount

    ):


        amount = Decimal(str(amount))

        self.total_profit += amount

        self.balance += amount

        self.equity = self.balance


    def add_loss(

        self,
        amount

    ):


        amount = Decimal(str(amount))

        self.total_loss += amount

        self.balance -= amount

        self.equity = self.balance


    def summary(self):


        return {

            "balance":

            float(self.balance),

            "equity":

            float(self.equity),

            "profit":

            float(self.total_profit),

            "loss":

            float(self.total_loss),

            "orders":

            len(self.orders)

        }