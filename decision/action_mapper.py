from __future__ import annotations


class ActionMapper:

    ACTIONS = {
        0: "HOLD",
        1: "BUY",
        2: "SELL",
    }

    def from_index(
        self,
        index: int,
    ):

        return self.ACTIONS.get(
            index,
            "HOLD",
        )

    def to_index(
        self,
        action: str,
    ):

        for idx, value in self.ACTIONS.items():

            if value == action:
                return idx

        return 0