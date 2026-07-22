from __future__ import annotations


class Ledger:

    def __init__(self):

        self.entries = []

    ###########################################################

    def record(

        self,

        fill,

    ):

        self.entries.append(fill)

    ###########################################################

    def all(self):

        return self.entries

    ###########################################################

    def clear(self):

        self.entries.clear()