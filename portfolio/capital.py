from __future__ import annotations

from decimal import Decimal


class CapitalManager:

    def __init__(
        self,
        initial_balance: Decimal,
    ):

        self.initial_balance = initial_balance

        self.cash = initial_balance

        self.locked = Decimal("0")

    @property
    def available(self):

        return self.cash - self.locked

    def reserve(
        self,
        amount: Decimal,
    ):

        if amount > self.available:
            return False

        self.locked += amount

        return True

    def release(
        self,
        amount: Decimal,
    ):

        self.locked -= amount

        if self.locked < 0:
            self.locked = Decimal("0")

    def deposit(
        self,
        amount: Decimal,
    ):

        self.cash += amount

    def withdraw(
        self,
        amount: Decimal,
    ):

        self.cash -= amount