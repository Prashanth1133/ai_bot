from decimal import Decimal


class BacktestPortfolio:

    def __init__(

        self,

        balance=Decimal("10000"),

    ):

        self.balance = balance

        self.equity = balance

        self.positions = {}