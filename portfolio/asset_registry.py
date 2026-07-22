from __future__ import annotations


class AssetRegistry:

    def __init__(self):

        self._assets = {}

    def register(

        self,

        symbol,

        asset,

    ):

        self._assets[symbol] = asset

    def get(self, symbol):

        return self._assets.get(symbol)

    def remove(self, symbol):

        self._assets.pop(symbol, None)

    def all(self):

        return list(self._assets.values())

    def clear(self):

        self._assets.clear()