from __future__ import annotations


class PositionBook:

    def __init__(self):

        self._positions = {}

    def add(
        self,
        position,
    ):

        self._positions[
            position.symbol
        ] = position

    def remove(
        self,
        symbol,
    ):

        self._positions.pop(
            symbol,
            None,
        )

    def get(
        self,
        symbol,
    ):

        return self._positions.get(
            symbol
        )

    def values(self):

        return list(
            self._positions.values()
        )

    def clear(self):

        self._positions.clear()