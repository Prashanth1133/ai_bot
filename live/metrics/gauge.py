from __future__ import annotations


class Gauge:

    def __init__(self):

        self.value = 0.0

    def set(
        self,
        value: float,
    ):

        self.value = value

    def increment(
        self,
        amount: float = 1.0,
    ):

        self.value += amount

    def decrement(
        self,
        amount: float = 1.0,
    ):

        self.value -= amount

    def get(self):

        return self.value