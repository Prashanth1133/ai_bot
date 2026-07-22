from __future__ import annotations


class AccountRegistry:

    def __init__(self):

        self._accounts = {}

    def register(
        self,
        account_id,
        account,
    ):

        self._accounts[
            account_id
        ] = account

    def get(
        self,
        account_id,
    ):

        return self._accounts.get(
            account_id
        )

    def remove(
        self,
        account_id,
    ):

        self._accounts.pop(
            account_id,
            None,
        )

    def accounts(self):

        return self._accounts

    def clear(self):

        self._accounts.clear()