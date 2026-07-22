from __future__ import annotations

from models.signal import Signal


class SignalRegistry:

    def __init__(self):

        self._signals = {}

    def update(
        self,
        signal: Signal,
    ):

        self._signals[
            signal.symbol
        ] = signal

    def get(
        self,
        symbol: str,
    ):

        return self._signals.get(symbol)

    def remove(
        self,
        symbol: str,
    ):

        self._signals.pop(
            symbol,
            None,
        )

    def clear(self):

        self._signals.clear()

    def all(self):

        return list(
            self._signals.values()
        )