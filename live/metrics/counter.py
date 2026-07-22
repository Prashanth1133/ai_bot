from __future__ import annotations


class Counter:

    def __init__(self):

        self.value = 0

    def increment(
        self,
        amount: int = 1,
    ):

        self.value += amount

    def reset(self):

        self.value = 0

    def get(self):

        return self.value