from __future__ import annotations


class AccountStream:

    def __init__(self):

        self.balance = {}

        self.positions = {}

    def update(self, payload):

        event = payload.get("e")

        if event == "ACCOUNT_UPDATE":

            for asset in payload["a"]["B"]:

                self.balance[
                    asset["a"]
                ] = asset

            for position in payload["a"]["P"]:

                self.positions[
                    position["s"]
                ] = position

    def get_balance(
        self,
        asset,
    ):

        return self.balance.get(asset)

    def get_position(
        self,
        symbol,
    ):

        return self.positions.get(symbol)