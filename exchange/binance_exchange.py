from __future__ import annotations


class BinanceExchange:

    ###########################################################

    async def place_order(

        self,

        symbol,

        side,

        quantity,

        price,

        stop_loss,

        take_profit,

    ):

        return {

            "symbol": symbol,

            "side": side,

            "quantity": quantity,

            "price": price,

            "stop_loss": stop_loss,

            "take_profit": take_profit,

            "status": "FILLED",

            "realized_pnl": 0.0,

        }

    ###########################################################

    async def account(self):

        return {

            "balance": 10000.0,

            "equity": 10000.0,

            "margin": 0.0,

        }

    ###########################################################

    async def positions(self):

        return []