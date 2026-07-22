from __future__ import annotations


class PortfolioManager:

    def __init__(self):

        self.balance = 0.0

        self.equity = 0.0

        self.margin = 0.0

        self.positions = {}

    ###########################################################

    def update_balance(

        self,

        balance,

        equity,

        margin,

    ):

        self.balance = balance

        self.equity = equity

        self.margin = margin

    ###########################################################

    def update_position(

        self,

        symbol,

        position,

    ):

        self.positions[symbol] = position

    ###########################################################

    def remove_position(

        self,

        symbol,

    ):

        self.positions.pop(symbol, None)

    ###########################################################

    def get_position(

        self,

        symbol,

    ):

        return self.positions.get(symbol)

    ###########################################################

    def snapshot(self):

        return {

            "balance": self.balance,

            "equity": self.equity,

            "margin": self.margin,

            "positions": self.positions,

        }