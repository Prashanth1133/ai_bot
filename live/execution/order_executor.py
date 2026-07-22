from __future__ import annotations


class OrderExecutor:

    def __init__(

        self,

        exchange,

    ):

        self.exchange = exchange

    ##########################################################

    async def execute(

        self,

        trade,

    ):

        return await self.exchange.place_order(

            symbol=trade.symbol,

            side=trade.side,

            quantity=trade.quantity,

            price=trade.entry_price,

            stop_loss=trade.stop_loss,

            take_profit=trade.take_profit,

        )