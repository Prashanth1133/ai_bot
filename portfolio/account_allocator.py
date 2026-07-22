from __future__ import annotations

from decimal import Decimal


class AccountAllocator:

    def allocate(

        self,

        accounts,

        capital: Decimal,

    ):

        if not accounts:

            return {}

        allocation = (

            capital

            / Decimal(len(accounts))

        )

        return {

            account: allocation

            for account in accounts

        }