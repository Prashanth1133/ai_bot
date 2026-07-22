from __future__ import annotations

from threading import RLock


class SymbolCache:

    def __init__(self):

        self._symbols = {}

        self._lock = RLock()

    def update(
        self,
        symbol: str,
        info: dict,
    ):

        with self._lock:
            self._symbols[symbol.upper()] = info

    def get(
        self,
        symbol: str,
    ):

        with self._lock:
            return self._symbols.get(symbol.upper())

    def exists(
        self,
        symbol: str,
    ):

        with self._lock:
            return symbol.upper() in self._symbols

    def remove(
        self,
        symbol: str,
    ):

        with self._lock:
            self._symbols.pop(symbol.upper(), None)

    def all(self):

        with self._lock:
            return dict(self._symbols)

    def clear(self):

        with self._lock:
            self._symbols.clear()