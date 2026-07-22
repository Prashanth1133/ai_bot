from decimal import Decimal


class CashManager:

    def __init__(self):

        self.cash = Decimal("0")

    def deposit(

        self,

        amount,

    ):

        self.cash += amount

    def withdraw(

        self,

        amount,

    ):

        self.cash -= amount