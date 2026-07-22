from __future__ import annotations


class SymbolManager:

    def __init__(self):

        self.active_symbol = None

    def set(
        self,
        symbol: str,
    ):

        self.active_symbol = symbol.upper()

    def get(self):

        return self.active_symbol

    def clear(self):

        self.active_symbol = None